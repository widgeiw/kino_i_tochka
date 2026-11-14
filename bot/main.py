
import asyncio
import os

from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")

dp = Dispatcher()


@dp.message(CommandStart())
async def start_handler(message: Message):
    await message.answer(
        "Привет! Добро пожаловать в «Кино и точка»!\n\n"
        "Здесь ты сможешь:\n"
        "- Искать фильмы\n"
        "- Отмечать просмотренные\n"
        "- Сохранять фильмы в список желаемого\n"
        "- Ставить оценки и писать отзывы"
    )


async def main():
    if not TOKEN:
        raise RuntimeError("BOT_TOKEN не найден в файле .env")

    bot = Bot(token=TOKEN)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())