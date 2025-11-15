from aiogram import Router, types, F
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from keyboards import main_menu_kb
from utils import add_help_request, get_user
from config import ADMIN_IDS
from utils import load_admins

router = Router()

class HelpState(StatesGroup):
    waiting_text = State()
    confirming = State()

@router.callback_query(F.data == "help")
async def help_start(callback: types.CallbackQuery):
    """Show static help/FAQ and allow user to choose to write a message for admins."""
    body = (
        "❓ Savollar:\n"
        "• Bot qanday ishlaydi?\n"
        "• QBC nima?\n"
        "• Premium nima?\n\n"
        "📧 Biz bilan bog'lanish:\n"
        "@support_username\n\n"
        "🐛 Muammoni xabar qiling:\n"
        "Agar muammo bo'lsa, adminni xabardor qiling.\n"
    )
    kb = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text="📝 Habar yozish", callback_data="help_write")],
        [types.InlineKeyboardButton(text="🔙 Orqaga", callback_data="main_menu")]
    ])
    try:
        await callback.message.edit_text(body, reply_markup=kb)
    except Exception:
        try:
            await callback.answer()
        except Exception:
            pass
    await callback.answer()

@router.callback_query(F.data == "help_write")
async def help_write(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text("Iltimos muammo yoki savolingizni qisqacha yozing:")
    await state.set_state(HelpState.waiting_text)
    await callback.answer()

@router.message(HelpState.waiting_text)
async def help_received(message: types.Message, state: FSMContext):
    text = (message.text or '').strip()
    if not text:
        await message.reply("Iltimos, xabar matnini kiriting.")
        return

    user = get_user(message.from_user.id)
    username = user.get('username') if user else message.from_user.username

    # Save request immediately and notify admins
    req = add_help_request(message.from_user.id, username, text)
    from utils import admins_ids_list
    admins = admins_ids_list()
    for adm in admins:
        try:
            await message.bot.send_message(adm, f"🆘 Yangi yordam so'rovi #{req['id']}\nFrom: @{username} ({req['user_id']})\n\n{text}")
        except Exception:
            pass

    await message.reply("✅ Sizning xabaringiz saqlandi va adminlarga yuborildi. Tez orada javob beriladi.")
    await state.clear()

@router.callback_query(F.data == "help_confirm_send", HelpState.confirming)
async def help_confirm_send(callback: types.CallbackQuery, state: FSMContext):
    # kept for backward compatibility but won't normally be used
    await callback.answer()

@router.callback_query(F.data == "help_cancel")
async def help_cancel(callback: types.CallbackQuery, state: FSMContext):
    try:
        await callback.message.edit_text("❌ Yordam so'rovi bekor qilindi.", reply_markup=main_menu_kb())
    except Exception:
        pass
    await state.clear()
    await callback.answer()
