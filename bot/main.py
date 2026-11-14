import asyncio
import os

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from dotenv import load_dotenv

from bot.keyboards import main_keyboard
from bot.states import SearchStates


load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")

dp = Dispatcher()


@dp.message(CommandStart())
async def start_handler(message: Message, state: FSMContext):
    await state.clear()

    await message.answer(
        "Привет! 🎬 Добро пожаловать в «Кино и точка»!\n\n"
        "Выбери, что хочешь сделать:",
        reply_markup=main_keyboard
    )


@dp.message(Command("cancel"))
async def cancel_handler(message: Message, state: FSMContext):
    await state.clear()

    await message.answer(
        "Действие отменено.",
        reply_markup=main_keyboard
    )


@dp.message(F.text == "🔎 Поиск фильма")
async def search_handler(message: Message, state: FSMContext):
    await state.set_state(SearchStates.waiting_for_title)

    await message.answer(
        "🔎 Введи название фильма, который хочешь найти.\n\n"
        "Для отмены отправь /cancel."
    )


@dp.message(F.text == "✅ Просмотрено")
async def watched_handler(message: Message, state: FSMContext):
    await state.clear()

    await message.answer(
        "✅ Здесь будет список просмотренных фильмов."
    )


@dp.message(F.text == "❤️ Хочу посмотреть")
async def wishlist_handler(message: Message, state: FSMContext):
    await state.clear()

    await message.answer(
        "❤️ Здесь будут фильмы, которые ты хочешь посмотреть."
    )


@dp.message(F.text == "👤 Мой профиль")
async def profile_handler(message: Message, state: FSMContext):
    await state.clear()

    await message.answer(
        "👤 Здесь будет твой профиль, оценки и отзывы."
    )


@dp.message(SearchStates.waiting_for_title, F.text)
async def movie_title_handler(message: Message, state: FSMContext):
    title = message.text.strip()

    if not title:
        await message.answer("Введи непустое название фильма.")
        return

    await state.clear()

    await message.answer(
        f"🔎 Ищем фильм: {title}\n\n"
        "Подключение к каталогу фильмов появится позже.",
        reply_markup=main_keyboard
    )


@dp.message(SearchStates.waiting_for_title)
async def invalid_title_handler(message: Message):
    await message.answer(
        "Пожалуйста, отправь название фильма текстом."
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