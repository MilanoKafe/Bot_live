import asyncio
import logging
from aiogram import Bot, Dispatcher, F, types
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommand
from config import BOT_TOKEN
from handlers import start, test, menu, admin, referral
from handlers import help as help_handler
from middleware import AntiCheatingMiddleware, TestStateMiddleware

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Bot instansiyasi
bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

# Middleware
dp.message.middleware(AntiCheatingMiddleware())
dp.message.middleware(TestStateMiddleware())

# Routerlar
dp.include_router(start.router)
dp.include_router(test.router)
dp.include_router(menu.router)
dp.include_router(referral.router)
dp.include_router(admin.router)
dp.include_router(help_handler.router)

async def set_commands():
    """Bot buyruqlarini o'rnatish"""
    commands = [
        BotCommand(command="start", description="Botni boshlash"),
        BotCommand(command="admin", description="Admin paneli"),
        BotCommand(command="help", description="Yordam"),
    ]
    await bot.set_my_commands(commands)

async def on_startup(dispatcher):
    """Bot startup"""
    await set_commands()
    logger.info("Bot boshlandi!")

async def on_shutdown(dispatcher):
    """Bot shutdown"""
    await bot.session.close()
    logger.info("Bot to'xtadi!")

async def main():
    """Asosiy funksiya"""
    await on_startup(dp)
    
    try:
        logger.info("Bot polling boshlandi...")
        await dp.start_polling(bot)
    except Exception as e:
        logger.error(f"Xato: {e}")
    finally:
        await on_shutdown(dp)

if __name__ == "__main__":
    asyncio.run(main())
