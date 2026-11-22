import unittest
from unittest.mock import AsyncMock, MagicMock

from aiogram.types import Message

from bot.api_client import BackendError
from bot.keyboards import movie_selection_keyboard
from bot.main import search_page_handler, navigation_handler


class StateStub:
    def __init__(self, data):
        self.data = data
        self.state = None

    async def get_data(self):
        return self.data.copy()

    async def update_data(self, **data):
        self.data.update(data)

    async def clear(self):
        self.data = {}
        self.state = None

    async def set_state(self, state):
        self.state = state


def callback(data):
    result = MagicMock()
    result.data = data
    result.answer = AsyncMock()
    result.message = MagicMock(spec=Message)
    result.message.answer = AsyncMock()
    return result


def search_data(page=1, pages=3):
    return {"page": page, "total_pages": pages,
            "results": [{"id": 1, "title": "Фильм"}]}


class NavigationTests(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.state = StateStub({"query": "Бэтмен", "search": search_data(), "token": "abc"})
        self.api = MagicMock()
        self.api.search_movies = AsyncMock(return_value=search_data(2))

    async def test_next_page_preserves_query(self):
        event = callback("page:abc:2")
        await search_page_handler(event, self.state, self.api)
        self.api.search_movies.assert_awaited_once_with("Бэтмен", 2)
        self.assertEqual(self.state.data["search"]["page"], 2)
        event.answer.assert_awaited_once()

    async def test_error_keeps_previous_results(self):
        self.api.search_movies.side_effect = BackendError("Недоступен")
        await search_page_handler(callback("page:abc:2"), self.state, self.api)
        self.assertEqual(self.state.data["search"]["page"], 1)

    async def test_stale_or_out_of_range_does_not_request_api(self):
        for data in ("page:old:2", "page:abc:0", "page:abc:501", "page:abc:bad"):
            await search_page_handler(callback(data), self.state, self.api)
        self.api.search_movies.assert_not_awaited()

    async def test_back_uses_cached_results(self):
        event = callback("results:abc")
        await search_page_handler(event, self.state, self.api)
        self.api.search_movies.assert_not_awaited()
        event.message.answer.assert_awaited_once()

    async def test_menu_clears_search(self):
        await navigation_handler(callback("nav:menu"), self.state)
        self.assertEqual(self.state.data, {})

    async def test_new_search_clears_old_buttons(self):
        await navigation_handler(callback("search:new"), self.state)
        self.assertEqual(self.state.data, {})
        self.assertIsNotNone(self.state.state)


class PagingKeyboardTests(unittest.TestCase):
    def page_buttons(self, page, pages):
        keyboard = movie_selection_keyboard([], page, pages, "abc")
        return [b.callback_data for row in keyboard.inline_keyboard for b in row]

    def test_boundaries_and_api_limit(self):
        self.assertNotIn("page:abc:0", self.page_buttons(1, 3))
        self.assertIn("page:abc:2", self.page_buttons(1, 3))
        self.assertNotIn("page:abc:4", self.page_buttons(3, 3))
        self.assertNotIn("page:abc:501", self.page_buttons(500, 1000))
        self.assertIn("page:abc:499", self.page_buttons(500, 1000))
