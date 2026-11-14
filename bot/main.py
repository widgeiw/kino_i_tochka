import asyncio
import os

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import Message
from dotenv import load_dotenv

from bot.keyboards import main_keyboard


load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")

dp = Dispatcher()


@dp.message(CommandStart())
async def start_handler(message: Message):
    await message.answer(
        "Привет! 🎬 Добро пожаловать в «Кино и точка»!\n\n"
        "Выбери, что хочешь сделать:",
        reply_markup=main_keyboard
    )


@dp.message(F.text == "🔎 Поиск фильма")
async def search_handler(message: Message):
    await message.answer(
        "🔎 Здесь ты сможешь искать фильмы по названию."
    )


@dp.message(F.text == "✅ Просмотрено")
async def watched_handler(message: Message):
    await message.answer(
        "✅ Здесь будет список просмотренных фильмов."
    )


@dp.message(F.text == "❤️ Хочу посмотреть")
async def wishlist_handler(message: Message):
    await message.answer(
        "❤️ Здесь будут фильмы, которые ты хочешь посмотреть."
    )


@dp.message(F.text == "👤 Мой профиль")
async def profile_handler(message: Message):
    await message.answer(
        "👤 Здесь будет твой профиль, оценки и отзывы."
    )


async def main():
    if not TOKEN:
        raise RuntimeError("BOT_TOKEN не найден в файле .env")

    bot = Bot(token=TOKEN)

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())