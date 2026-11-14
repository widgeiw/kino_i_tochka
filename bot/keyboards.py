from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🔎 Поиск фильма"),
            KeyboardButton(text="✅ Просмотрено")
        ],
        [
            KeyboardButton(text="❤️ Хочу посмотреть"),
            KeyboardButton(text="👤 Мой профиль")
        ]
    ],
    resize_keyboard=True
)
