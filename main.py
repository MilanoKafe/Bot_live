import asyncio

from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message

TOKEN = ("8165812265:AAEJXGhC2x9dV6OnB8lFxWWJMVqa0HfpOxA")

dp = Dispatcher()


# Command handler
@dp.message(Command("start"))
async def command_start_handler(message: Message) -> None:
    await message.answer("Salom bot serverga qoyildi test muvaffaiyatli otdi")

@dp.message(Command("help"))
async def command_help_handler(message: Message) -> None:
    await message.answer("Bu yerda yordam boladi")

@dp.message(Command("info"))
async def command_info_handler(message: Message) -> None:
    await message.answer("Bu esa haqida")

@dp.message(Command("community"))
async def command_community_handler(message: Message) -> None:
    await message.answer("Bu yerda jamo boladi")

@dp.message(Command("contact"))
async def command_contact_handler(message: Message) -> None:
    await message.answer("Bu aloqa bolmi.")

@dp.message(Command("admin"))
async def command_admin_handler(message: Message) -> None:
    await message.answer("Bu esa admin admin linki boladi")

@dp.message(Command("dashboard"))
async def command_dashboard_handler(message: Message) -> None:
    await message.answer("Admin dashboard")


# Run the bot
async def main() -> None:
    bot = Bot(token=TOKEN)
    await dp.start_polling(bot)

print("Bot ishga tushdi")


if __name__ == "__main__":
    asyncio.run(main())
          