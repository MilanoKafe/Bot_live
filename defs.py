from aiogram import Bot, Dispatcher
from aiogram.enums import parse_mode
from aiogram.types import Message
import os
from dotenv import load_dotenv
from states import Sign_up
from aiogram.fsm.context import FSMContext


load_dotenv()

group_id = os.getenv('group_id')

async def admin(message: Message,bot : Bot):
    user = message.from_user
    bio = await bot.get_chat(message.from_user.id)

    user_photo = await  message.from_user.get_profile_photos()
    log_text = (
        f"👤 Foydalanuvchi {message.from_user.mention_html(user.first_name)}\n"
        f"🆔 ID: {user.id}\n"
        f"ℹ️ Ismi: {user.first_name}, To‘liq ismi: {user.full_name}\n"
        f"🚹 Chat ID: {message.chat.id}\n"
        f"📛user name: @{user.username}\n"
        f"\n"
    )
    log_text_txt = (
        f"👤 Yangi user\n"
        f"🆔 ID: {user.id}\n"
        f"ℹ️ Ismi: {user.first_name}\n➖To‘liq ismi: {user.full_name}\n"
        f"🚹 Chat ID: {message.chat.id}\n"
        f"📛user name: @{user.username}\n"
        f"\n"
    )
    if bio.bio:log_text += f"Bio: {bio.bio}\n——————————————————————————————————————————————————————————————\n"
    else:log_text += f"——————————————————————————————————————————————————————————————\n"
    if bio.bio:log_text_txt += f"Bio: {bio.bio}\n——————————————————————————————————————————————————————————————\n"
    else:log_text_txt += f"——————————————————————————————————————————————————————————————\n"
    if user_photo:
        await bot.send_photo(group_id,user_photo.photos[0][-1].file_id,caption=log_text,parse_mode='HTML')

    else:
        await bot.send_message(group_id,log_text,parse_mode='HTML')
    with open("log.txt", 'a',encoding='utf-8') as f:
        f.write(log_text_txt)
    return  log_text

async def user_help(message: Message,bot : Bot):
    help_message = f"""
    <b>Botdan foydalanish yoriqnomasi</b>
    
    /start - botni ishga tushuradi
    /info - foydalanuvchi haqidagi maumotlarni taqdim etadi
    /help - botdan foydalanish yoriqnomasi
"""
    await message.answer(help_message,parse_mode='HTML')

async def user_info(message: Message,bot : Bot):
    user = message.from_user
    bio = await bot.get_chat(message.from_user.id)

    user_photo = await  message.from_user.get_profile_photos()
    log_text = (
        f"👤 Foydalanuvchi {message.from_user.mention_html(user.first_name)}\n"
        f"🆔 ID: {user.id}\n"
        f"ℹ️ Ismi: {user.first_name}, To‘liq ismi: {user.full_name}\n"
        f"🚹 Chat ID: {message.chat.id}\n"
        f"📛user name: @{user.username}\n"
        f"\n"
    )
    if bio.bio:log_text += f"Bio: {bio.bio}\n——————————————————————————————————————————————————————————————\n"
    else:log_text += f"——————————————————————————————————————————————————————————————\n"
    if user_photo:
        await bot.send_photo(group_id,user_photo.photos[0][-1].file_id,caption=log_text,parse_mode='HTML')

    await message.answer(log_text,parse_mode='HTML')

async def alert(message: Message,bot : Bot):
    await message.answer("Botdan foydalanishda faqat tugmalar bilan ishlang iltimos")

async def start(message: Message,bot : Bot,state: FSMContext):
    await message.answer("Ismingiz")
    await state.set_state(Sign_up.name)


async def sign_up_name(message: Message,bot : Bot,state:FSMContext):
    await state.update_data(name=message.text)
    await message.answer(f"Ismingiz qabul qilindi: {message.text}")
    await message.answer("Yoshingizni yozing")
    await state.set_state(Sign_up.age)

async def sign_up_age(message: Message,bot : Bot,state:FSMContext):
    await state.update_data(age=message.text)
    data = await state.get_data()
    await message.answer(f"""Sizni malumotingiz\nIsmingiz{data.get("name")}\nYoshingiz{data.get("age")}""")
    await state.clear()