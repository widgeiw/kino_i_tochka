from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton)


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


def movie_selection_keyboard(movies: list[dict]) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text=f"{index}. {movie['title'][:60]}",
            callback_data=f"movie:{movie['id']}",
        )]
        for index, movie in enumerate(movies[:20], start=1)
    ])
