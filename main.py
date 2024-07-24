import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters.command import Command
from aiogram.fsm.storage.memory import MemoryStorage
from config import BOT_TOKEN as token
from channel_requirements import CheckSubRequirement, channels_dict
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from weather import get_weather
from random import choice

logging.basicConfig(level=logging.INFO)
bot = Bot(token=token)
dp = Dispatcher(storage=MemoryStorage())

@dp.message(Command('start'))
async def start(message: types.Message):
    await message.answer_photo(
        photo="https://images.unsplash.com/photo-1561470508-fd4df1ed90b2?q=80&w=1776&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
        caption=f"Bizning ob-havo haqidagi botimizga xush kelibsiz!\nBuning uchun biror bir mamlakat yoki shahar nomini kiriting.",
        )

# Channel subbing
@dp.message(CheckSubRequirement())
async def checking_requirement(message: types.Message) -> None:
    keyboard = []
    for button_text, url in channels_dict.items():
        button = InlineKeyboardButton(text=button_text, url=url)
        keyboard.append([button])  # Each button in its own row
    keyboard.append([InlineKeyboardButton(text="Tekshirish ✅", callback_data='check_sub')])
    markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
    await message.answer("Diqqat!\nBotdan foydalanish uchun ushbu kanallarga obuna bo'ling!", reply_markup=markup)

@dp.callback_query(F.data == "check_sub", CheckSubRequirement())
async def process_callback_check(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id, text="Iltimos barcha kanallarga obuna bo'ling 🙏")

@dp.callback_query(F.data == "check_sub")
async def process_callback_check(callback_query: types.CallbackQuery):
    await callback_query.message.answer('Siz endi botdan foydalanishingiz mumkin!\nMarhamat kerakli manzilni kiriting')

# Get data from api

photos_list = [
    "https://a.storyblok.com/f/176292/1536x864/5d5c0ecaf5/uchshie-goroda-dlya-zhizni-kakoj-gorod-vybrat-dlya-prozhivaniya-1.jpeg",
    "https://images5.alphacoders.com/456/456536.jpg",
    "https://images.unsplash.com/photo-1477959858617-67f85cf4f1df?fm=jpg&q=60&w=3000&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxleHBsb3JlLWZlZWR8MXx8fGVufDB8fHx8fA%3D%3D",
    "https://4kwallpapers.com/images/walls/thumbs_2t/4320.jpg",
    "https://4kwallpapers.com/images/walls/thumbs_2t/4320.jpg",
    "https://wallpapers.com/images/hd/city-desktop-znar9th5rt5q1pxs.jpg",
    "https://wallpapers.com/images/featured/new-york-city-5oaa14h4mw6w3o71.webp",
    "https://images.wallpaperscraft.com/image/single/city_aerial_view_road_156925_300x168.jpg",
    "https://images.pexels.com/photos/1139556/pexels-photo-1139556.jpeg?cs=srgb&dl=pexels-zhangkaiyv-1139556.jpg&fm=jpg",
    "https://wallpaper.forfun.com/fetch/6c/6c0cf748db116fabaa70199a35327258.jpeg",
]

@dp.message(F.text)
async def handle_text(message: types.Message) -> None:
    random_photo = choice(photos_list)
    location = message.text.lower().strip()
    data = get_weather(location)
    await message.answer_photo(photo=random_photo, caption=data, parse_mode='HTML')

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
