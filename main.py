
from aiogram import Bot, Dispatcher, types
from  asyncio import  run
from aiogram.types import Message, BotCommand
from aiogram.filters import Command

import defs
import states
from defs import user_info,user_help,alert,start
import  os
from dotenv import load_dotenv

load_dotenv()


group_id = os.getenv("group_id")

dp = Dispatcher()







async def main():
    dp.message.register(defs.start,defs.admin, Command('start'))
    dp.message.register(defs.user_info, Command('info'))
    dp.message.register(defs.user_help, Command('help'))
    dp.message.register(defs.sign_up_name, states.Sign_up.name)
    dp.message.register(defs.sign_up_age, states.Sign_up.age)


    dp.message.register(defs.alert)
    bot = Bot("8296333807:AAEaP4ZPAJ-oU5aCzA4gaHeHuCCb4xrecEI")
    await bot.set_my_commands([
        BotCommand(command='start',description='Botni ishga tushurish'),
        BotCommand(command='info', description='User haqida malumot'),
        BotCommand(command='help', description='Bot boyicha yordam')
    ])
    await dp.start_polling(bot, polling_timeout=2)


print("Bot ishladi")

if __name__ == "__main__":
    run(main())
