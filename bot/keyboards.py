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


def navigation_keyboard(token: str = "", back: bool = False) -> InlineKeyboardMarkup:
    rows = []
    if back:
        rows.append([InlineKeyboardButton(text="⬅️ К результатам", callback_data=f"results:{token}")])
    rows.append([
        InlineKeyboardButton(text="🔎 Новый поиск", callback_data="search:new"),
        InlineKeyboardButton(text="🏠 В меню", callback_data="nav:menu"),
    ])
    return InlineKeyboardMarkup(inline_keyboard=rows)


def movie_selection_keyboard(movies: list[dict], page: int = 1,
                             total_pages: int = 1, token: str = "") -> InlineKeyboardMarkup:
    rows = [
        [InlineKeyboardButton(
            text=f"{index}. {movie['title'][:60]}",
            callback_data=f"movie:{token}:{movie['id']}",
        )]
        for index, movie in enumerate(movies[:20], start=1)
    ]
    paging = []
    if page > 1:
        paging.append(InlineKeyboardButton(text="⬅️ Назад", callback_data=f"page:{token}:{page - 1}"))
    if page < min(total_pages, 500):
        paging.append(InlineKeyboardButton(text="Вперёд ➡️", callback_data=f"page:{token}:{page + 1}"))
    if paging:
        rows.append(paging)
    rows.extend(navigation_keyboard().inline_keyboard)
    return InlineKeyboardMarkup(inline_keyboard=rows)
