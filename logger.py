import logging
import sys
import io
from datetime import datetime

# Ensure stdout uses UTF-8 so emojis don't crash Windows console
try:
    # Python 3.7+ has reconfigure
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    try:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    except Exception:
        pass

# Logging setup with UTF-8 file handler
fh = logging.FileHandler('bot.log', encoding='utf-8')
sh = logging.StreamHandler(stream=sys.stdout)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
sh.setFormatter(formatter)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(fh)
logger.addHandler(sh)

def log_user_action(user_id, action, details=""):
    """Foydalanuvchi amallarini yozib qolish"""
    logger.info(f"User {user_id} - Action: {action} - Details: {details}")

# Exportga logger'ni qo'shish
__all__ = ['logger', 'log_user_action']
