from aiogram import Router, types, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext
from utils import get_user, update_user
from keyboards import main_menu_kb
from logger import log_user_action

router = Router()

@router.callback_query(F.data == "main_menu")
async def main_menu(callback: types.CallbackQuery, state: FSMContext):
    """Asosiy menyu"""
    await state.clear()
    await callback.message.edit_text(
        "📌 Asosiy menyu:\n\n"
        "Qanday qilmoqchisiz?",
        reply_markup=main_menu_kb()
    )
    try:
        await callback.answer()
    except TelegramBadRequest:
        # ignore stale/expired callback query errors
        pass

@router.callback_query(F.data == "balance")
async def balance(callback: types.CallbackQuery):
    """Balansni ko'rsatish"""
    user_id = callback.from_user.id
    user = get_user(user_id)
    
    if user:
        qbc = user.get('qbc', 0)
        total_questions = user.get('total_questions', 0)
        correct_answers = user.get('correct_answers', 0)
        referrals_count = len(user.get('referrals', []))
        
        text = (
            f"💰 Sizning balansingiz:\n\n"
            f"💎 QBC: {qbc}\n"
            f"📝 Jami testlar: {total_questions}\n"
            f"✅ To'g'ri javoblar: {correct_answers}\n"
            f"👥 Referrallar: {referrals_count}\n\n"
            f"📢 Referral kodi: <code>{user_id}</code>\n"
            f"Har bir referral uchun: +0.2 QBC"
        )
    else:
        text = "❌ Foydalanuvchi ma'lumoti topilmadi."
    
    await callback.message.edit_text(
        text,
        parse_mode="HTML",
        reply_markup=types.InlineKeyboardMarkup(inline_keyboard=[
            [types.InlineKeyboardButton(text="👥 Referralga taklif qilish", callback_data="share_referral")],
            [types.InlineKeyboardButton(text="🔙 Orqaga", callback_data="main_menu")]
        ])
    )
    try:
        await callback.answer()
    except TelegramBadRequest:
        pass

@router.callback_query(F.data == "guide")
async def guide(callback: types.CallbackQuery):
    """Qo'llanma"""
    text = (
        "📖 Quiz Bot Qo'llanmasi:\n\n"
        "1️⃣ <b>Test ishlash:</b>\n"
        "   • Yo'nalish tanlang (Backend, Frontend, Grafika, Savodhonlik)\n"
        "   • Savollarga javob bering\n"
        "   • Har bir to'g'ri javob: +0.5 QBC\n"
        "   • Vaqt limiti: 15 soniya\n\n"
        "2️⃣ <b>Balans:</b>\n"
        "   • Sizning QBC balansingizni ko'ring\n"
        "   • Statistikani ko'ring\n\n"
        "3️⃣ <b>Referral:</b>\n"
        "   • Referral kodingizni do'stlaringizga yuboring\n"
        "   • Har bir referral uchun +0.2 QBC\n\n"
        "4️⃣ <b>Premium:</b>\n"
        "   • QBC xarij qilib premium bo'ling\n"
        "   • Premium: cheksiz test, reklama yo'q"
    )
    
    await callback.message.edit_text(
        text,
        parse_mode="HTML",
        reply_markup=types.InlineKeyboardMarkup(inline_keyboard=[
            [types.InlineKeyboardButton(text="🔙 Orqaga", callback_data="main_menu")]
        ])
    )
    try:
        await callback.answer()
    except TelegramBadRequest:
        pass


@router.callback_query(F.data == "premium")
async def premium(callback: types.CallbackQuery):
    """Premium"""
    user_id = callback.from_user.id
    user = get_user(user_id)
    
    if user and user.get('is_premium'):
        text = "✅ Siz allaqachon Premium foydalanuchisiz!"
        kb = types.InlineKeyboardMarkup(inline_keyboard=[
            [types.InlineKeyboardButton(text="🔙 Orqaga", callback_data="main_menu")]
        ])
    else:
        text = (
            "⭐ Premium Obuna:\n\n"
            "Premium narxlari:\n"
            "• 1 yil (to'liq): 200 QBC\n\n"
            "Premium imkoniyatlari:\n"
            "✅ Cheksiz test\n"
            "✅ Reklama yo'q\n"
            "✅ QBC 1.5x ko'paytirilgan\n\n"
            "Premiumni sotib olish uchun 200 QBC to'lang."
        )
        kb = types.InlineKeyboardMarkup(inline_keyboard=[
            [types.InlineKeyboardButton(text="💳 Premiumni sotib olish (200 QBC)", callback_data="premium_buy_200")],
            [types.InlineKeyboardButton(text="🔙 Orqaga", callback_data="main_menu")]
        ])

    await callback.message.edit_text(
        text,
        reply_markup=kb
    )
    try:
        await callback.answer()
    except TelegramBadRequest:
        pass


@router.callback_query(F.data == "premium_buy_200")
async def premium_buy_200(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user = get_user(user_id)
    if not user:
        await callback.answer("❌ Foydalanuvchi topilmadi!", show_alert=True)
        return

    qbc = user.get('qbc', 0)
    cost = 200
    if qbc < cost:
        await callback.answer("❌ Sizda yetarli QBC yo'q!", show_alert=True)
        return

    update_user(user_id, qbc=qbc - cost, is_premium=True)
    await callback.message.edit_text("✅ Siz premiumni sotib oldingiz. Rahmat!", reply_markup=types.InlineKeyboardMarkup(inline_keyboard=[[types.InlineKeyboardButton(text="🔙 Asosiy menyu", callback_data="main_menu")]]))
    await callback.answer()
