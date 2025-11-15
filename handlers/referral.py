from aiogram import Router, types, F
from utils import get_user, update_user, add_referral, load_users, save_users
from keyboards import main_menu_kb
from logger import log_user_action

router = Router()

@router.message(F.text.startswith("/start ref_"))
async def referral_start(message: types.Message):
    """Referral link bilan start"""
    user_id = message.from_user.id
    username = message.from_user.username
    
    # Referral kodini olish
    try:
        ref_code = int(message.text.split("_")[1])
    except:
        await message.answer("❌ Noto'g'ri referral link!")
        return
    
    # Foydalanuvchini tekshirish
    user = get_user(user_id)
    
    if user:
        if user.get('referred_by'):
            await message.answer("❌ Siz allaqachon referral bilan ro'yxatdan o'tgansiz!")
        else:
            # Referral qo'shish
            if add_referral(ref_code, user_id):
                update_user(user_id, referred_by=ref_code)
                await message.answer(
                    f"✅ Referral muvaffaqiyatli qo'shildi!\n\n"
                    f"Referrer: {ref_code}\n"
                    f"Siz +0.2 QBC oldingiz",
                    reply_markup=main_menu_kb()
                )
                log_user_action(user_id, "Referral qabul qildi", f"ref: {ref_code}")
            else:
                await message.answer("❌ Referral xatosi!")
    else:
        # Yangi foydalanuvchi, referral bilan yaratish
        from utils import create_user
        create_user(user_id, username, ref_code)
        
        if add_referral(ref_code, user_id):
            await message.answer(
                f"✅ Xush kelibsiz!\n"
                f"Referral qabul qilindi, +0.2 QBC\n\n"
                f"Referrer: {ref_code}",
                reply_markup=main_menu_kb()
            )
            log_user_action(user_id, "Yangi foydalanuvchi (referral)", f"ref: {ref_code}")

@router.callback_query(F.data == "share_referral")
async def share_referral(callback: types.CallbackQuery):
    """Referral kodini ulashish"""
    user_id = callback.from_user.id
    user = get_user(user_id)
    
    if not user:
        await callback.answer("❌ Foydalanuvchi topilmadi!", show_alert=True)
        return
    
    referral_link = f"https://t.me/YOUR_BOT_USERNAME?start=ref_{user_id}"
    
    text = (
        f"📢 Sizning referral kodingiz:\n\n"
        f"<code>{user_id}</code>\n\n"
        f"Referral link:\n"
        f"Har bir referral uchun: +0.2 QBC\n"
        f"Sizning referrallar: {len(user.get('referrals', []))}"
    )
    
    await callback.message.edit_text(
        text,
        parse_mode="HTML",
        reply_markup=types.InlineKeyboardMarkup(inline_keyboard=[
            [types.InlineKeyboardButton(text="📋 Nusxalash", callback_data="copy_referral")],
            [types.InlineKeyboardButton(text="🔙 Orqaga", callback_data="main_menu")]
        ])
    )
    await callback.answer()

@router.callback_query(F.data == "copy_referral")
async def copy_referral(callback: types.CallbackQuery):
    """Referral kodini nusxalash"""
    user_id = callback.from_user.id
    
    await callback.answer(
        f"✅ Kod nusxalandi: {user_id}\n\n"
        f"Do'stlaringizga yuboring!",
        show_alert=True
    )
