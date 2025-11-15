import asyncio
import random
from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from utils import get_user, update_user, get_questions_by_category
from keyboards import test_category_kb, start_or_back_kb, main_menu_kb
from logger import log_user_action

router = Router()

class TestState(StatesGroup):
    selecting_category = State()
    confirming_start = State()
    answering_question = State()
    test_active = State()

@router.callback_query(F.data == "test_start")
async def test_start(callback: types.CallbackQuery, state: FSMContext):
    """Test boshlashni tanlash"""
    await callback.message.edit_text(
        "📚 Qaysi yo'nalishda test ishlashni xohlaysiz?",
        reply_markup=test_category_kb()
    )
    await state.set_state(TestState.selecting_category)
    await callback.answer()

@router.callback_query(F.data.startswith("test_"), TestState.selecting_category)
async def test_category_selected(callback: types.CallbackQuery, state: FSMContext):
    """Kategoriya tanlandi"""
    category_map = {
        "test_backend": "backend",
        "test_frontend": "frontend",
        "test_grafika": "grafika",
        "test_savodhonlik": "savodhonlik",
    }
    
    data = callback.data
    if data not in category_map:
        await callback.answer()
        return
    
    category = category_map[data]
    
    # Savollarni tekshirish va foydalanuvchiga berilganlarga filter qo'llash (per-category)
    user = get_user(callback.from_user.id)
    attempted_all_raw = user.get('attempted_questions', {}) if user else {}
    # Prevent retake if user already completed this category
    completed = user.get('completed_tests', []) if user else []
    if category in completed:
        await callback.answer("❌ Siz bu kategoriyani allaqachon tugatgansiz. Qayta ishlash mumkin emas.", show_alert=True)
        return
    # handle legacy list format by converting to empty dict
    attempted_all = attempted_all_raw if isinstance(attempted_all_raw, dict) else {}
    attempted = attempted_all.get(category, [])
    questions = [q for q in get_questions_by_category(category) if q['id'] not in attempted]
    if not questions:
        await callback.answer("❌ Ushbu kategoriyada siz uchun yangi savollar qolmadi!", show_alert=True)
        return

    await state.update_data(category=category, questions=questions, question_index=0, correct_count=0, attempted_questions=attempted)
    
    category_names = {
        "backend": "Backend",
        "frontend": "Frontend",
        "grafika": "Grafika",
        "savodhonlik": "Savodhonlik"
    }
    
    await callback.message.edit_text(
        f"✅ {category_names[category]} yo'nalishini tanladingiz!\n\n"
        f"Jami savol: {len(questions)}\n"
        f"Har bir to'g'ri javob: +0.5 QBC\n"
        f"Vaqt limiti: 15 soniya\n\n"
        "Boshlashga tayormi?",
        reply_markup=start_or_back_kb()
    )
    await state.set_state(TestState.confirming_start)
    await callback.answer()

@router.callback_query(F.data == "test_start_begin", TestState.confirming_start)
async def test_begin(callback: types.CallbackQuery, state: FSMContext):
    """Test boshlandi"""
    data = await state.get_data()
    questions = data.get('questions', [])
    category = data.get('category', '')
    user_id = callback.from_user.id
    
    log_user_action(user_id, "Test boshladi", f"category: {category}")
    
    await state.set_state(TestState.test_active)
    await send_question(callback.message, state, user_id)
    await callback.answer()

async def send_question(message, state: FSMContext, user_id):
    """Savolni yuborish"""
    data = await state.get_data()
    question_index = data.get('question_index', 0)
    correct_count = data.get('correct_count', 0)

    # Recompute remaining questions for this category at send time to avoid repeats
    category = data.get('category', '')
    # load fresh questions and filter out those the user already attempted in this category
    all_questions = get_questions_by_category(category)
    # get latest attempted list from user file (in case it changed)
    try:
        user = get_user(user_id)
        user_attempted_all = user.get('attempted_questions', {}) if user else {}
        user_attempted = user_attempted_all.get(category, []) if isinstance(user_attempted_all, dict) else []
    except Exception:
        user_attempted = []
    # Build remaining list
    remaining = [q for q in all_questions if q['id'] not in user_attempted]

    # original questions list (as set at test start) for total count
    original_questions = data.get('questions', [])
    total_for_display = len(original_questions) if original_questions else len(remaining)

    if question_index >= len(remaining):
        # Test tugadi (no remaining questions)
        await finish_test(message, state, user_id, correct_count, total_for_display, category)
        return

    question = remaining[question_index]
    question_id = question['id']
    answers = question['answers']

    # Persist attempted per-category
    try:
        user = get_user(user_id)
        if user:
            user_attempted_all = user.get('attempted_questions', {}) if isinstance(user.get('attempted_questions', {}), dict) else {}
            cat_list = user_attempted_all.get(category, [])
            if question_id not in cat_list:
                cat_list.append(question_id)
                user_attempted_all[category] = cat_list
                update_user(user_id, attempted_questions=user_attempted_all)
    except Exception:
        pass

    # Shuffle answers
    shuffled_answers = answers.copy()
    random.shuffle(shuffled_answers)

    # Build keyboard
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=shuffled_answers[i]['text'], callback_data=f"answer_{question_id}_{i}")]
        for i in range(len(shuffled_answers))
    ])
    kb.inline_keyboard.append([InlineKeyboardButton(text="🔙 Orqaga (test bekor qilish)", callback_data="cancel_test")])

    text = (
        f"❓ Savol {question_index + 1}/{total_for_display}\n\n"
        f"{question['question']}\n\n"
        f"⏱️ Vaqti: 15 soniya"
    )

    await message.edit_text(text, reply_markup=kb)

    # Save current shuffled answers and question id so handler can verify correctness
    await state.update_data(question_index=question_index, time_started=asyncio.get_event_loop().time(), current_shuffled=shuffled_answers, current_question_id=question_id)

    # Auto-skip after timeout
    async def auto_skip():
        await asyncio.sleep(15)
        current_data = await state.get_data()
        if current_data.get('question_index') == question_index:
            # User didn't answer - move on
            await state.update_data(question_index=question_index + 1)
            try:
                await send_question(message, state, user_id)
            except:
                pass

    asyncio.create_task(auto_skip())

@router.callback_query(F.data.startswith("answer_"), TestState.test_active)
async def answer_question(callback: types.CallbackQuery, state: FSMContext):
    """Javob berildi"""
    user_id = callback.from_user.id
    data = await state.get_data()
    question_index = data.get('question_index', 0)
    correct_count = data.get('correct_count', 0)

    # Parse callback (format: answer_<question_id>_<index>)
    answer_data = callback.data.replace("answer_", "").split("_")
    try:
        qid = int(answer_data[0])
        answer_index = int(answer_data[-1])
    except Exception:
        await callback.answer("❌ Xato javob!")
        return

    current_shuffled = data.get('current_shuffled', [])
    current_qid = data.get('current_question_id')

    if not current_shuffled or answer_index >= len(current_shuffled) or qid != current_qid:
        await callback.answer("❌ Xato yoki muddati tugagan javob!")
        return

    selected = current_shuffled[answer_index]
    is_correct = selected.get('correct', False)
    if is_correct:
        correct_count += 1
        user = get_user(user_id)
        if user:
            new_qbc = user.get('qbc', 0) + 0.5
            update_user(user_id, qbc=new_qbc, total_questions=user.get('total_questions', 0) + 1, correct_answers=user.get('correct_answers', 0) + 1)

        text = "✅ To'g'ri javob!"
    else:
        user = get_user(user_id)
        if user:
            update_user(user_id, total_questions=user.get('total_questions', 0) + 1)

        # top to'g'ri javob xabarini shuffled ro'yxatdan olish
        correct_text = next((a['text'] for a in current_shuffled if a.get('correct')), "Noma'lum")
        text = f"❌ Noto'g'ri javob!\n\nTo'g'ri javob: {correct_text}"

    try:
        await callback.message.edit_text(text)
    except:
        pass

    await asyncio.sleep(1.5)  # Javobni ko'rish uchun vaqt

    # Keyingi savolga o'tish
    await state.update_data(question_index=question_index + 1, correct_count=correct_count)
    await send_question(callback.message, state, user_id)

    await callback.answer()

@router.callback_query(F.data == "cancel_test", TestState.test_active)
async def cancel_test(callback: types.CallbackQuery, state: FSMContext):
    """Test bekor qilish"""
    user_id = callback.from_user.id
    log_user_action(user_id, "Test bekor qilindi", "")
    
    await state.clear()
    await callback.message.edit_text(
        "❌ Test bekor qilindi.\n\n"
        "Asosiy menyuga qaytingiz.",
        reply_markup=main_menu_kb()
    )
    await callback.answer()

@router.callback_query(F.data == "test_category")
async def back_to_category(callback: types.CallbackQuery, state: FSMContext):
    """Kategoriya tanlashga qaytish"""
    await state.set_state(TestState.selecting_category)
    await callback.message.edit_text(
        "📚 Qaysi yo'nalishda test ishlashni xohlaysiz?",
        reply_markup=test_category_kb()
    )
    await callback.answer()

async def finish_test(message, state: FSMContext, user_id, correct_count, total_questions, category=None):
    """Test tugadi, natijani ko'rsatish"""
    # mark category as completed so user cannot retake
    try:
        user = get_user(user_id)
        if user:
            comps = user.get('completed_tests', []) if isinstance(user.get('completed_tests', []), list) else []
            if category and category not in comps:
                comps.append(category)
                update_user(user_id, completed_tests=comps)
    except Exception:
        pass
    percentage = (correct_count / total_questions * 100) if total_questions > 0 else 0
    total_qbc = correct_count * 0.5
    
    text = (
        f"🎉 Test tugadi!\n\n"
        f"📊 Natija:\n"
        f"To'g'ri javoblar: {correct_count}/{total_questions}\n"
        f"Foiz: {percentage:.1f}%\n"
        f"Foydalangiz QBC: +{total_qbc}\n\n"
        f"Yana test ishlashni xohlaysizmi?"
    )
    
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📝 Yana test", callback_data="test_start")],
        [InlineKeyboardButton(text="🔙 Asosiy menyu", callback_data="main_menu")]
    ])
    
    await message.edit_text(text, reply_markup=kb)
    await state.clear()
    
    log_user_action(user_id, "Test tugadi", f"To'g'ri: {correct_count}/{total_questions}")
