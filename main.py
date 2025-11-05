
from aiogram import Bot, Dispatcher, types
from  asyncio import  run
from aiogram.types import Message, BotCommand
from aiogram.filters import Command

import defs
import states
from defs import user_info,user_help,alert,start


group_id = -1003212923751

dp = Dispatcher()







async def main():
    dp.message.register(defs.start,defs.admin, Command('start'))
    dp.message.register(defs.user_info, Command('info'))
    dp.message.register(defs.user_help, Command('help'))
    dp.message.register(defs.sign_up_name, states.Sign_up.name)
    dp.message.register(defs.sign_up_age, states.Sign_up.age)


    dp.message.register(defs.alert)
    bot = Bot("8109704243:AAEkr728OeqOIObZCUtoqfazdTQrmgydNYw")
    await bot.set_my_commands([
        BotCommand(command='start',description='Botni ishga tushurish'),
        BotCommand(command='info', description='User haqida malumot'),
        BotCommand(command='help', description='Bot boyicha yordam')
    ])
    await dp.start_polling(bot, polling_timeout=2)


print("Bot ishladi")

if __name__ == "__main__":
    run(main())


