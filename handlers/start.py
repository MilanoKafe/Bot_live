from aiogram import Router, types, F, Dispatcher
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from utils import get_user, create_user, load_users
from keyboards import main_menu_kb
from filters import check_channel_subscription, get_subscribe_message
from logger import log_user_action
from config import CHANNEL_URL

router = Router()

@router.message(CommandStart())
async def start_command(message: types.Message, state: FSMContext):
    """Start buyrug'i"""
    user_id = message.from_user.id
    username = message.from_user.username
    
    # Kanal obunasini tekshirish
    is_subscribed = await check_channel_subscription(message.bot, user_id)
    
    if not is_subscribed:
        await message.answer(
            get_subscribe_message(),
            parse_mode="HTML",
            reply_markup=types.InlineKeyboardMarkup(inline_keyboard=[
                [types.InlineKeyboardButton(text="✅ Obuna bo'ldim", callback_data="check_subscription")]
            ])
        )
        return
    
    # Foydalanuvchini tekshirish yoki yaratish
    user = get_user(user_id)
    if not user:
        create_user(user_id, username)
        log_user_action(user_id, "Yangi foydalanuvchi", f"username: {username}")
        # Notify admin about new user
        # Notify all admins about the new user (dynamic admins)
        try:
            from utils import admins_ids_list
            admins = admins_ids_list()
            for adm in admins:
                try:
                    await message.bot.send_message(
                        adm,
                        f"👤 Yangi foydalanuvchi ro'yxatdan o'tdi:\n@{username} ({user_id})"
                    )
                except Exception:
                    pass
        except Exception:
            pass
        await message.answer(
            f"👋 Assalomualikum, {username}!\n\n"
            "Quiz Bot-ga xush kelibsiz! 🎉\n\n"
            "Siz test ishlashni boshlashingiz mumkin.",
            reply_markup=main_menu_kb()
        )
    else:
        log_user_action(user_id, "Start qayta", f"username: {username}")
        await message.answer(
            f"👋 Qayta xush kelibsiz, {username}! 🎉\n\n"
            "Qanday qilmoqchisiz?",
            reply_markup=main_menu_kb()
        )
    
    await state.clear()

@router.callback_query(F.data == "check_subscription")
async def check_subscription_callback(callback: types.CallbackQuery):
    """Obunani qayta tekshirish"""
    user_id = callback.from_user.id
    is_subscribed = await check_channel_subscription(callback.bot, user_id)
    
    if is_subscribed:
        user = get_user(user_id)
        if not user:
            create_user(user_id, callback.from_user.username)
        await callback.message.delete()
        await callback.message.answer(
            f"✅ Rahmat obuna bo'lganingiz uchun! 🎉\n\n"
            f"Salom, {callback.from_user.first_name}!",
            reply_markup=main_menu_kb()
        )
    else:
        await callback.answer(
            "❌ Siz hali kanalga obuna bo'lmagansiz!",
            show_alert=True
        )
