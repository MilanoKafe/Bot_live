from aiogram import types, F
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def main_menu_kb():
    """Asosiy menyu tugmasi"""
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📝 Test ishlash", callback_data="test_start")],
        [InlineKeyboardButton(text="💰 Balans", callback_data="balance")],
        [InlineKeyboardButton(text="📖 Qo'llanma", callback_data="guide")],
        [InlineKeyboardButton(text="🆘 Yordam", callback_data="help")],
        [InlineKeyboardButton(text="⭐ Premium", callback_data="premium")]
    ])
    return kb

def test_category_kb():
    """Test kategoriyasini tanlash"""
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Backend", callback_data="test_backend")],
        [InlineKeyboardButton(text="Frontend", callback_data="test_frontend")],
        [InlineKeyboardButton(text="Grafika", callback_data="test_grafika")],
        [InlineKeyboardButton(text="Savodhonlik", callback_data="test_savodhonlik")],
        [InlineKeyboardButton(text="🔙 Orqaga", callback_data="main_menu")]
    ])
    return kb

def start_or_back_kb():
    """Test boshlash yoki orqaga qaytish"""
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="▶️ Boshlash", callback_data="test_start_begin")],
        [InlineKeyboardButton(text="🔙 Orqaga", callback_data="main_menu")]
    ])
    return kb

def answers_kb(answers, question_id):
    """Javob tugmalari"""
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=ans['text'], callback_data=f"answer_{question_id}_{i}")]
        for i, ans in enumerate(answers)
    ])
    kb.inline_keyboard.append([InlineKeyboardButton(text="🔙 Orqaga", callback_data="test_category")])
    return kb

def admin_menu_kb(is_owner: bool = False, admin_level: str | None = None):
    """Admin menyu. If `is_owner` is True, show owner-only settings.

    `admin_level` can be 'owner', 'full', 'user_admin', 'question_admin' to control visibility.
    """
    kb_buttons = []

    # Stats and user management available to full and user_admin and owner
    if admin_level in (None, 'owner', 'full', 'user_admin'):
        kb_buttons.append([InlineKeyboardButton(text="📊 Statistika", callback_data="admin_stats")])
        kb_buttons.append([InlineKeyboardButton(text="👥 Foydalanuvchilar", callback_data="admin_list_users")])
        kb_buttons.append([InlineKeyboardButton(text="⛔ Ban foydalanuvchi", callback_data="admin_ban_user")])
        kb_buttons.append([InlineKeyboardButton(text="✅ Unban foydalanuvchi", callback_data="admin_unban_user")])

    # Question management available to full and question_admin and owner
    if admin_level in (None, 'owner', 'full', 'question_admin'):
        kb_buttons.append([InlineKeyboardButton(text="➕ Savol qo'shish", callback_data="admin_add_question")])

    # Grant and broadcast for full and owner
    if admin_level in (None, 'owner', 'full'):
        kb_buttons.append([InlineKeyboardButton(text="💸 QBC berish", callback_data="admin_grant_qbc")])
        kb_buttons.append([InlineKeyboardButton(text="📢 Reklama yuborish", callback_data="admin_broadcast")])

    # Help requests visible to admins responsible for users/full/owner
    if admin_level in (None, 'owner', 'full', 'user_admin'):
        kb_buttons.append([InlineKeyboardButton(text="🆘 Yordam so'rovlari", callback_data="admin_help_list")])

    kb = InlineKeyboardMarkup(inline_keyboard=kb_buttons)

    if is_owner:
        # Owner-only items
        kb.inline_keyboard.append([InlineKeyboardButton(text="➕ Admin qo'shish", callback_data="admin_add_admin")])
        kb.inline_keyboard.append([InlineKeyboardButton(text="➖ Admin o'chirish", callback_data="admin_remove_admin")])
        kb.inline_keyboard.append([InlineKeyboardButton(text="⚙️ Muhim sozlamalar", callback_data="admin_settings")])

    kb.inline_keyboard.append([InlineKeyboardButton(text="🔙 Orqaga", callback_data="main_menu")])
    return kb


def admin_quick_grant_kb():
    """Quick grant amounts for admin QBC giving"""
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="1 QBC", callback_data="admin_grant_qbc_amt_1"), InlineKeyboardButton(text="2 QBC", callback_data="admin_grant_qbc_amt_2")],
        [InlineKeyboardButton(text="3 QBC", callback_data="admin_grant_qbc_amt_3"), InlineKeyboardButton(text="5 QBC", callback_data="admin_grant_qbc_amt_5")],
        [InlineKeyboardButton(text="10 QBC", callback_data="admin_grant_qbc_amt_10")],
        [InlineKeyboardButton(text="✍️ Qo'lda yuborish", callback_data="admin_grant_qbc_manual")],
        [InlineKeyboardButton(text="🔙 Orqaga", callback_data="admin_back")]
    ])
    return kb

def yes_no_kb(callback_prefix):
    """Ha/Yo'q tugmalari"""
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ Ha", callback_data=f"{callback_prefix}_yes"),
            InlineKeyboardButton(text="❌ Yo'q", callback_data=f"{callback_prefix}_no")
        ]
    ])
    return kb
