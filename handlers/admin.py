from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from config import ADMIN_IDS, OWNER_ID
from utils import get_user_statistics, get_user, load_users, add_question, load_questions, update_user, is_admin, add_admin, remove_admin, load_admins, get_admin_level, admins_ids_list
from keyboards import main_menu_kb, admin_menu_kb, admin_quick_grant_kb
from logger import log_user_action, logger
from datetime import datetime, timedelta
import asyncio
import logging

router = Router()

class AdminState(StatesGroup):
    adding_question_category = State()
    adding_question_new_category = State()
    adding_question_text = State()
    adding_question_answers = State()
    adding_question_correct = State()
    sending_broadcast = State()
    granting_qbc = State()
    banning_user = State()
    unbanning_user = State()
    adding_admin = State()
    removing_admin = State()
    choosing_admin_level = State()

# use utils.is_admin for admin checks; owner id is available as OWNER_ID

@router.message(F.text == "/admin")
async def admin_panel(message: types.Message):
    """Admin paneli"""
    if not is_admin(message.from_user.id):
        await message.answer("❌ Siz admin emassiz!")
        return

    is_owner = (message.from_user.id == OWNER_ID)
    admin_level = get_admin_level(message.from_user.id)
    await message.answer(
        "👨‍💼 Admin Paneli:",
        reply_markup=admin_menu_kb(is_owner=is_owner, admin_level=admin_level)
    )

@router.callback_query(F.data == "admin_stats")
async def admin_stats(callback: types.CallbackQuery):
    """Statistika"""
    if not is_admin(callback.from_user.id):
        await callback.answer("❌ Siz admin emassiz!", show_alert=True)
        return
    
    stats = get_user_statistics()
    users = stats['users']
    
    # Kunlik, haftalik va oylik statistika
    now = datetime.now()
    today = now.date()
    week_ago = now - timedelta(days=7)
    month_ago = now - timedelta(days=30)
    
    today_users = 0
    week_users = 0
    month_users = 0
    
    for user in users:
        try:
            created_at = datetime.fromisoformat(user.get('created_at', ''))
            if created_at.date() == today:
                today_users += 1
            if created_at > week_ago:
                week_users += 1
            if created_at > month_ago:
                month_users += 1
        except:
            pass
    
    # Online foydalanuvchilar (approximate - har kim)
    online_count = len(users)
    
    text = (
        f"📊 Statistika:\n\n"
        f"👥 Jami foydalanuvchilar: {stats['total_users']}\n"
        f"⭐ Premium foydalanuvchilar: {stats['premium_users']}\n"
        f"💎 Jami QBC: {stats['total_qbc']:.1f}\n\n"
        f"📈 O'sish:\n"
        f"🕐 Bugun: {today_users}\n"
        f"📅 Shu hafta: {week_users}\n"
        f"🗓️ Shu oy: {month_users}\n\n"
        f"🟢 Online: ~{online_count} (online)"
    )
    
    await callback.message.edit_text(
        text,
        reply_markup=types.InlineKeyboardMarkup(inline_keyboard=[
            [types.InlineKeyboardButton(text="🔙 Orqaga", callback_data="admin_back")]
        ])
    )
    await callback.answer()


@router.callback_query(F.data == "admin_help_list")
async def admin_help_list(callback: types.CallbackQuery):
    if not is_admin(callback.from_user.id):
        await callback.answer("❌ Siz admin emassiz!", show_alert=True)
        return

    from utils import load_help_requests
    reqs = load_help_requests()
    if not reqs:
        await callback.answer("Yordam so'rovlari topilmadi.", show_alert=True)
        return

    lines = [f"{r['id']}. @{r.get('username','-')} ({r['user_id']}) - {r['status']}" for r in reqs]
    text = "🆘 Yordam so'rovlari:\n\n" + "\n".join(lines)
    kb = types.InlineKeyboardMarkup(inline_keyboard=[[types.InlineKeyboardButton(text="🔙 Orqaga", callback_data="admin_back")]])
    await callback.message.edit_text(text, reply_markup=kb)
    await callback.answer()

@router.callback_query(F.data == "admin_add_question")
async def admin_add_question_start(callback: types.CallbackQuery, state: FSMContext):
    """Yangi savol qo'shish boshlash"""
    if not is_admin(callback.from_user.id):
        await callback.answer("❌ Siz admin emassiz!", show_alert=True)
        return
    # Owner gets to choose web or bot for adding questions; other admins use bot flow
    if callback.from_user.id == OWNER_ID:
        kb = types.InlineKeyboardMarkup(inline_keyboard=[
            [types.InlineKeyboardButton(text="📱 Bot orqali qo'shish", callback_data="admin_add_method_bot")],
            [types.InlineKeyboardButton(text="🌐 Web orqali qo'shish", callback_data="admin_add_method_web")],
            [types.InlineKeyboardButton(text="🔙 Orqaga", callback_data="admin_back")]
        ])
        await callback.message.edit_text("📚 Savol qanday yo'l bilan qo'shilsin?", reply_markup=kb)
        await callback.answer()
        return

    # Non-owner: proceed with bot flow (choose category/create new)
    cats = load_questions().keys()
    kb_buttons = []
    for cat in cats:
        kb_buttons.append([types.InlineKeyboardButton(text=cat, callback_data=f"add_q_cat_{cat}")])
    # Add option to create new category
    kb_buttons.append([types.InlineKeyboardButton(text="🆕 Yangi kategoriya", callback_data="add_q_cat_new")])
    kb = types.InlineKeyboardMarkup(inline_keyboard=kb_buttons)

    await callback.message.edit_text(
        "📚 Savol qaysi kategoriyaga tegishli?",
        reply_markup=kb
    )
    await state.set_state(AdminState.adding_question_category)
    await callback.answer()

@router.callback_query(F.data.startswith("add_q_cat_"), AdminState.adding_question_category)
async def admin_add_question_category(callback: types.CallbackQuery, state: FSMContext):
    """Kategoriya tanlandi"""
    key = callback.data.replace("add_q_cat_", "")

    if key == "new":
        # Ask admin to send new category name
        await callback.message.edit_text("🆕 Yangi kategoriya nomini yozing:")
        await state.set_state(AdminState.adding_question_new_category)
        await callback.answer()
        return

    category = key
    await state.update_data(category=category, answers=[])
    await callback.message.edit_text("✍️ Savolni yozing:")
    await state.set_state(AdminState.adding_question_text)
    await callback.answer()


@router.message(AdminState.adding_question_new_category)
async def admin_add_question_new_category(message: types.Message, state: FSMContext):
    """Admin provided a new category name"""
    category = message.text.strip()
    if not category:
        await message.answer("❌ Bo'sh kategoriya nomi yuborilmadi.")
        return

    # Save category name and proceed to ask for question text
    await state.update_data(category=category, answers=[])
    await message.answer("✍️ Endi savol matnini yozing:")
    await state.set_state(AdminState.adding_question_text)

@router.message(AdminState.adding_question_text)
async def admin_add_question_text(message: types.Message, state: FSMContext):
    """Savol matni"""
    await state.update_data(question_text=message.text)
    
    await message.answer(
        "📝 Endi 4 ta javobni yozing.\n"
        "Har bir javobni alohida qatorga yozing:\n\n"
        "Javob 1\n"
        "Javob 2\n"
        "Javob 3\n"
        "Javob 4"
    )
    await state.set_state(AdminState.adding_question_answers)

@router.message(AdminState.adding_question_answers)
async def admin_add_question_answers(message: types.Message, state: FSMContext):
    """Javoblar"""
    answers_text = message.text.strip().split('\n')
    
    if len(answers_text) != 4:
        await message.answer("❌ Aniq 4 ta javob kiritish kerak!")
        return
    
    answers = [{"text": ans.strip(), "correct": False} for ans in answers_text]
    await state.update_data(answers=answers)
    
    # Javoblarni ko'rsatish
    kb = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text=f"{i+1}-javob", callback_data=f"add_q_correct_{i}")]
        for i in range(4)
    ])
    
    answer_list = "\n".join([f"{i+1}. {ans['text']}" for i, ans in enumerate(answers)])
    
    await message.answer(
        f"Qaysi javob to'g'ri?\n\n{answer_list}",
        reply_markup=kb
    )
    await state.set_state(AdminState.adding_question_correct)

@router.callback_query(F.data.startswith("add_q_correct_"), AdminState.adding_question_correct)
async def admin_add_question_correct(callback: types.CallbackQuery, state: FSMContext):
    """To'g'ri javobni tanlash"""
    correct_index = int(callback.data.replace("add_q_correct_", ""))
    
    data = await state.get_data()
    answers = data['answers']
    answers[correct_index]['correct'] = True
    
    category = data['category']
    question_text = data['question_text']
    
    # Savolni qo'shish
    add_question(category, question_text, answers)
    
    await callback.message.edit_text(
        "✅ Savol muvaffaqiyatli qo'shildi!\n\n"
        f"Kategoriya: {category}\n"
        f"Savol: {question_text}\n"
        f"To'g'ri javob: {answers[correct_index]['text']}"
    )
    
    await state.clear()
    await callback.answer()

@router.callback_query(F.data == "admin_broadcast")
async def admin_broadcast_start(callback: types.CallbackQuery, state: FSMContext):
    """Reklama yuborish"""
    if not is_admin(callback.from_user.id):
        await callback.answer("❌ Siz admin emassiz!", show_alert=True)
        return
    
    await callback.message.edit_text(
        "📢 Reklama matnini yozing:"
    )
    await state.set_state(AdminState.sending_broadcast)
    await callback.answer()


@router.callback_query(F.data == "admin_list_users")
async def admin_list_users(callback: types.CallbackQuery):
    """Foydalanuvchilar ro'yxatini ko'rsatish"""
    if not is_admin(callback.from_user.id):
        await callback.answer("❌ Siz admin emassiz!", show_alert=True)
        return

    users = load_users()
    if not users:
        await callback.answer("Foydalanuvchilar topilmadi.", show_alert=True)
        return

    # Show top 10 by QBC
    top = sorted(users, key=lambda u: u.get('qbc', 0), reverse=True)[:10]
    lines = [f"{i+1}. @{u.get('username','-')} ({u['id']}): {u.get('qbc',0)} QBC" for i, u in enumerate(top)]
    text = "📋 Top foydalanuvchilar:\n\n" + "\n".join(lines)
    await callback.message.edit_text(text, reply_markup=types.InlineKeyboardMarkup(inline_keyboard=[[types.InlineKeyboardButton(text="🔙 Orqaga", callback_data="admin_back")]]))
    await callback.answer()


@router.callback_query(F.data == "admin_grant_qbc")
async def admin_grant_qbc_start(callback: types.CallbackQuery, state: FSMContext):
    if not is_admin(callback.from_user.id):
        await callback.answer("❌ Siz admin emassiz!", show_alert=True)
        return

    # Show quick grant buttons or allow manual input
    await callback.message.edit_text(
        "📥 Qaysi miqdor berilsin?\nYoki 'Qo'lda yuborish' tugmasi bilan qo'lda yuboring.",
        reply_markup=admin_quick_grant_kb()
    )
    await state.set_state(AdminState.granting_qbc)
    await callback.answer()


@router.callback_query(F.data == "admin_ban_user")
async def admin_ban_user_start(callback: types.CallbackQuery, state: FSMContext):
    if not is_admin(callback.from_user.id):
        await callback.answer("❌ Siz admin emassiz!", show_alert=True)
        return

    await callback.message.edit_text("⛔ Iltimos: ban qilish uchun foydalanuvchi ID sini yuboring (masalan: 7613242496)")
    await state.set_state(AdminState.banning_user)
    await callback.answer()


@router.message(AdminState.banning_user)
async def admin_ban_user_do(message: types.Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        await message.answer("❌ Siz admin emassiz!")
        await state.clear()
        return

    try:
        user_id = int(message.text.strip())
    except:
        await message.answer("❌ Iltimos to'g'ri user_id yuboring.")
        return

    user = get_user(user_id)
    if not user:
        await message.answer("❌ Foydalanuvchi topilmadi.")
        await state.clear()
        return

    update_user(user_id, is_banned=True)
    await message.answer(f"✅ {user_id} bloklandi.")
    await state.clear()


@router.callback_query(F.data == "admin_unban_user")
async def admin_unban_user_start(callback: types.CallbackQuery, state: FSMContext):
    if not is_admin(callback.from_user.id):
        await callback.answer("❌ Siz admin emassiz!", show_alert=True)
        return

    await callback.message.edit_text("✅ Iltimos: unban qilish uchun foydalanuvchi ID sini yuboring (masalan: 7613242496)")
    await state.set_state(AdminState.unbanning_user)
    await callback.answer()


@router.message(AdminState.unbanning_user)
async def admin_unban_user_do(message: types.Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        await message.answer("❌ Siz admin emassiz!")
        await state.clear()
        return

    try:
        user_id = int(message.text.strip())
    except:
        await message.answer("❌ Iltimos to'g'ri user_id yuboring.")
        return

    user = get_user(user_id)
    if not user:
        await message.answer("❌ Foydalanuvchi topilmadi.")
        await state.clear()
        return

    update_user(user_id, is_banned=False)
    await message.answer(f"✅ {user_id} ning bloklanishi olib tashlandi.")
    await state.clear()


@router.message(AdminState.granting_qbc)
async def admin_grant_qbc_do(message: types.Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        await message.answer("❌ Siz admin emassiz!")
        await state.clear()
        return

    # Check if an amount was preselected in state (from quick buttons)
    data = await state.get_data()
    preset_amount = data.get('grant_amount')

    # If preset_amount exists, message text should be user_id
    if preset_amount is not None:
        try:
            user_id = int(message.text.strip())
            amount = float(preset_amount)
        except Exception:
            await message.answer("❌ Iltimos to'g'ri user_id yuboring.")
            return
    else:
        # fallback to manual 'user_id amount'
        parts = message.text.strip().split()
        if len(parts) != 2:
            await message.answer("❌ Format xato. 'user_id amount' shaklida yuboring.")
            return
        try:
            user_id = int(parts[0])
            amount = float(parts[1])
        except:
            await message.answer("❌ ID yoki summa noto'g'ri.")
            return

    user = get_user(user_id)
    if not user:
        await message.answer("❌ Foydalanuvchi topilmadi.")
        await state.clear()
        return

    new_qbc = user.get('qbc', 0) + amount
    update_user(user_id, qbc=new_qbc)
    await message.answer(f"✅ {user_id} ga {amount} QBC qo'shildi. Yangi balans: {new_qbc}")
    await state.clear()


@router.callback_query(F.data.startswith("admin_grant_qbc_amt_"), AdminState.granting_qbc)
async def admin_grant_qbc_preset(callback: types.CallbackQuery, state: FSMContext):
    """Handle preset amount buttons and ask for user_id."""
    if not is_admin(callback.from_user.id):
        await callback.answer("❌ Siz admin emassiz!", show_alert=True)
        return

    try:
        amt = callback.data.replace("admin_grant_qbc_amt_", "")
        amt_val = float(amt)
    except Exception:
        await callback.answer("Xato miqdor.", show_alert=True)
        return

    # store preset in state and ask admin to send user_id
    await state.update_data(grant_amount=amt_val)
    await callback.message.edit_text(f"📥 Endi foydalanuvchi ID sini yuboring. Tanlangan miqdor: {amt_val} QBC")
    await callback.answer()


@router.callback_query(F.data == "admin_grant_qbc_manual", AdminState.granting_qbc)
async def admin_grant_qbc_manual_cb(callback: types.CallbackQuery, state: FSMContext):
    if not is_admin(callback.from_user.id):
        await callback.answer("❌ Siz admin emassiz!", show_alert=True)
        return

    await callback.message.edit_text("📥 Iltimos: 'user_id amount' formatida yuboring (masalan: 7613242496 10)")
    # clear any preset
    await state.update_data(grant_amount=None)
    await callback.answer()

@router.message(AdminState.sending_broadcast)
async def admin_broadcast_send(message: types.Message, state: FSMContext):
    """Reklamani barcha foydalanuvchilarga yuborish"""
    # Use the bot instance attached to the message to avoid importing main
    bot = message.bot
    broadcast_text = message.text
    users = load_users()
    success_count = 0
    failed_count = 0
    
    await message.answer(
        "📤 Reklama yuborilmoqda...\n"
        f"Jami: {len(users)} ta foydalanuvchiga"
    )
    
    for user in users:
        try:
            await bot.send_message(
                user['id'],
                f"📢 <b>Yangi reklama:</b>\n\n{broadcast_text}",
                parse_mode="HTML"
            )
            success_count += 1
        except Exception as e:
            failed_count += 1
            logger.error(f"Broadcast xatosi {user['id']}: {e}")
        
        # Spam bo'lmasligi uchun
        await asyncio.sleep(0.1)
    
    await message.answer(
        f"✅ Reklama yuborildi!\n"
        f"Muvaffaq: {success_count}\n"
        f"Xatoli: {failed_count}"
    )
    
    await state.clear()

@router.callback_query(F.data == "admin_back")
async def admin_back(callback: types.CallbackQuery):
    """Admin paneliga qaytish"""
    if not is_admin(callback.from_user.id):
        await callback.answer("❌ Siz admin emassiz!", show_alert=True)
        return
    is_owner = (callback.from_user.id == OWNER_ID)
    admin_level = get_admin_level(callback.from_user.id)
    await callback.message.edit_text(
        "👨‍💼 Admin Paneli:",
        reply_markup=admin_menu_kb(is_owner=is_owner, admin_level=admin_level)
    )
    await callback.answer()


@router.callback_query(F.data == "admin_add_admin")
async def admin_add_admin_start(callback: types.CallbackQuery, state: FSMContext):
    # Only owner can add admins
    if callback.from_user.id != OWNER_ID:
        await callback.answer("❌ Faqat owner amallarni bajarishi mumkin!", show_alert=True)
        return

    await callback.message.edit_text("➕ Iltimos, qo'shmoqchi bo'lgan adminning user_id sini yuboring:")
    await state.set_state(AdminState.adding_admin)
    await callback.answer()


@router.callback_query(F.data == "admin_add_method_web")
async def admin_add_method_web(callback: types.CallbackQuery):
    if callback.from_user.id != OWNER_ID:
        await callback.answer("❌ Faqat owner amallarni bajarishi mumkin!", show_alert=True)
        return

    from config import ADMIN_WEB_TOKEN
    url = f"http://127.0.0.1:5001/?token={ADMIN_WEB_TOKEN}"
    await callback.message.edit_text(f"🌐 Web-admin ochildi: {url}\nIltimos brauzerda oching. (Local serverni `python web_admin.py` bilan ishga tushiring)")
    await callback.answer()


@router.callback_query(F.data == "admin_add_method_bot")
async def admin_add_method_bot(callback: types.CallbackQuery, state: FSMContext):
    # proceed with bot-based add-question flow (show categories)
    if not is_admin(callback.from_user.id):
        await callback.answer("❌ Siz admin emassiz!", show_alert=True)
        return

    cats = load_questions().keys()
    kb_buttons = []
    for cat in cats:
        kb_buttons.append([types.InlineKeyboardButton(text=cat, callback_data=f"add_q_cat_{cat}")])
    kb_buttons.append([types.InlineKeyboardButton(text="🆕 Yangi kategoriya", callback_data="add_q_cat_new")])
    kb = types.InlineKeyboardMarkup(inline_keyboard=kb_buttons)

    await callback.message.edit_text(
        "📚 Savol qaysi kategoriyaga tegishli?",
        reply_markup=kb
    )
    await state.set_state(AdminState.adding_question_category)
    await callback.answer()


@router.message(AdminState.adding_admin)
async def admin_add_admin_do(message: types.Message, state: FSMContext):
    if message.from_user.id != OWNER_ID:
        await message.answer("❌ Faqat owner amallarni bajarishi mumkin!")
        await state.clear()
        return

    try:
        uid = int(message.text.strip())
    except Exception:
        await message.answer("❌ Iltimos to'g'ri user_id yuboring.")
        return

    # ask for level selection
    kb = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text="Savol admin (faqat savol qo'shish/tahrir)", callback_data=f"set_admin_level_{uid}_question")],
        [types.InlineKeyboardButton(text="User admin (ban/unban/stat)", callback_data=f"set_admin_level_{uid}_user")],
        [types.InlineKeyboardButton(text="Full admin (ko'p funksiyalar)", callback_data=f"set_admin_level_{uid}_full")],
        [types.InlineKeyboardButton(text="Bekor qilish", callback_data="admin_add_cancel")]
    ])
    await message.answer(f"ID: {uid}\nIltimos admin darajasini tanlang:", reply_markup=kb)
    await state.update_data(pending_admin_uid=uid)
    await state.set_state(AdminState.choosing_admin_level)


@router.callback_query(F.data.startswith("set_admin_level_"), AdminState.choosing_admin_level)
async def admin_set_level(callback: types.CallbackQuery, state: FSMContext):
    if callback.from_user.id != OWNER_ID:
        await callback.answer("❌ Faqat owner amallarni bajarishi mumkin!", show_alert=True)
        return

    data = callback.data.replace("set_admin_level_", "")
    # format: <uid>_<type>
    parts = data.split("_")
    if len(parts) < 2:
        await callback.answer("Xato format", show_alert=True)
        return
    try:
        uid = int(parts[0])
    except Exception:
        await callback.answer("Xato user id", show_alert=True)
        return
    typ = parts[1]
    lvl = 'user_admin'
    if typ == 'question':
        lvl = 'question_admin'
    elif typ == 'user':
        lvl = 'user_admin'
    elif typ == 'full':
        lvl = 'full'

    ok = add_admin(uid, level=lvl)
    if ok:
        await callback.message.edit_text(f"✅ {uid} admin sifatida qo'shildi (level: {lvl}).")
    else:
        await callback.message.edit_text(f"ℹ️ {uid} ni qo'shishda xatolik yoki allaqachon admin.")

    await state.clear()


@router.callback_query(F.data == "admin_add_cancel", AdminState.choosing_admin_level)
async def admin_add_cancel(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text("🛑 Qo'shish bekor qilindi.", reply_markup=admin_menu_kb(is_owner=(callback.from_user.id==OWNER_ID)))
    await state.clear()


@router.callback_query(F.data == "admin_add_admin")
async def admin_add_admin_start(callback: types.CallbackQuery, state: FSMContext):
    # Only owner can add admins
    if callback.from_user.id != OWNER_ID:
        await callback.answer("❌ Faqat owner amallarni bajarishi mumkin!", show_alert=True)
        return

    await callback.message.edit_text("➕ Iltimos, qo'shmoqchi bo'lgan adminning user_id sini yuboring:")
    await state.set_state(AdminState.adding_admin)
    await callback.answer()
 


@router.callback_query(F.data == "admin_remove_admin")
async def admin_remove_admin_start(callback: types.CallbackQuery, state: FSMContext):
    if callback.from_user.id != OWNER_ID:
        await callback.answer("❌ Faqat owner amallarni bajarishi mumkin!", show_alert=True)
        return

    await callback.message.edit_text("➖ Iltimos, o'chirmoqchi bo'lgan adminning user_id sini yuboring:")
    await state.set_state(AdminState.removing_admin)
    await callback.answer()


@router.message(AdminState.removing_admin)
async def admin_remove_admin_do(message: types.Message, state: FSMContext):
    if message.from_user.id != OWNER_ID:
        await message.answer("❌ Faqat owner amallarni bajarishi mumkin!")
        await state.clear()
        return

    try:
        uid = int(message.text.strip())
    except Exception:
        await message.answer("❌ Iltimos to'g'ri user_id yuboring.")
        return

    ok = remove_admin(uid)
    if ok:
        await message.answer(f"✅ {uid} admin sifatida olib tashlandi.")
    else:
        await message.answer(f"ℹ️ {uid} adminlar ro'yxatida topilmadi yoki xatolik.")
    await state.clear()
