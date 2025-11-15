from aiogram import types
from config import BOT_TOKEN, CHANNEL_ID, CHANNEL_URL
import logging

logger = logging.getLogger(__name__)

async def check_channel_subscription(bot, user_id):
    """Foydalanuvchi kanalga obuna qilganmi tekshirish.

    Use the provided `bot` instance to avoid importing `main`.
    """
    try:
        member = await bot.get_chat_member(CHANNEL_ID, user_id)
        return member.status in ['member', 'administrator', 'creator']
    except Exception as e:
        logger.error(f"Channel subscription check error: {e}")
        return False

def get_subscribe_message():
    """Obuna xabari"""
    text = (
        "👋 Assalomualikum!\n\n"
        "Ushbu botdan foydalanish uchun avval kanalga obuna bo'lishingiz kerak:\n\n"
        f"<a href='{CHANNEL_URL}'>📢 Kanalga obuna bo'lish</a>\n\n"
        "Obuna bo'lgandan so'ng /start buyrug'ini qayta yuboring."
    )
    return text
