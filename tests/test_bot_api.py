import unittest

import httpx

from bot.api_client import BackendError, MovieAPI


class MovieAPITests(unittest.IsolatedAsyncioTestCase):
    async def request_with(self, handler, query="Interstellar"):
        async with httpx.AsyncClient(
            trust_env=False, base_url="http://backend:8000", transport=httpx.MockTransport(handler)
        ) as client:
            return await MovieAPI(client).search_movies(query)

    async def test_search_contract(self):
        def handler(request):
            self.assertEqual(request.url.path, "/api/v1/movies/search")
            self.assertEqual(request.url.params["query"], "Интерстеллар & кино")
            self.assertEqual(request.url.params["page"], "1")
            return httpx.Response(200, json={"page": 1, "total_pages": 1, "results": [{"id": 1, "title": "Фильм"}]})
        data = await self.request_with(handler, "Интерстеллар & кино")
        self.assertEqual(data["results"][0]["id"], 1)

    async def test_second_page_contract(self):
        def handler(request):
            self.assertEqual(request.url.params["page"], "2")
            return httpx.Response(200, json={"page": 2, "total_pages": 3, "results": []})
        async with httpx.AsyncClient(
            trust_env=False, base_url="http://backend:8000",
            transport=httpx.MockTransport(handler),
        ) as client:
            data = await MovieAPI(client).search_movies("Бэтмен", 2)
        self.assertEqual(data["page"], 2)

    async def test_empty_results(self):
        data = await self.request_with(lambda r: httpx.Response(200, json={"page": 1, "total_pages": 0, "results": []}))
        self.assertEqual(data["results"], [])

    async def test_http_errors(self):
        for status in (422, 502, 503, 504):
            with self.subTest(status=status), self.assertRaises(BackendError):
                await self.request_with(lambda r: httpx.Response(status))

    async def test_network_errors(self):
        for error in (httpx.ReadTimeout, httpx.ConnectError):
            def handler(request):
                raise error("network failure", request=request)
            with self.subTest(error=error), self.assertRaises(BackendError):
                await self.request_with(handler)

    async def test_invalid_response(self):
        for payload in ({}, [], {"results": [None]}, {"results": [{"title": 1}]}):
            with self.subTest(payload=payload), self.assertRaises(BackendError):
                await self.request_with(lambda r: httpx.Response(200, json=payload))
        with self.assertRaises(BackendError):
            await self.request_with(lambda r: httpx.Response(200, text="not json"))

    async def test_movie_details_contract(self):
        def handler(request):
            self.assertEqual(request.url.path, "/api/v1/movies/157336")
            return httpx.Response(200, json={
                "id": 157336, "title": "Интерстеллар", "overview": "Описание",
                "vote_average": 8.4, "genres": ["Фантастика"], "runtime": 169,
                "poster_url": None, "release_date": "2014-11-05",
            })
        async with httpx.AsyncClient(
            trust_env=False, base_url="http://backend:8000",
            transport=httpx.MockTransport(handler),
        ) as client:
            movie = await MovieAPI(client).movie_details(157336)
        self.assertEqual(movie.runtime, 169)
        self.assertIsNone(movie.poster_url)

    async def test_movie_details_error_and_invalid_data(self):
        for response in (httpx.Response(404), httpx.Response(200, json={}),
                         httpx.Response(200, text="invalid json")):
            async with httpx.AsyncClient(
                trust_env=False, base_url="http://backend:8000",
                transport=httpx.MockTransport(lambda r: response),
            ) as client:
                with self.assertRaises(BackendError):
                    await MovieAPI(client).movie_details(1)


class MovieCardTests(unittest.TestCase):
    def test_missing_fields_and_long_description(self):
        from bot.movie_card import MovieDetail, format_movie_card
        movie = MovieDetail(id=1, title="Фильм", overview="", vote_average=0, genres=[])
        text = format_movie_card(movie)
        self.assertIn("год неизвестен", text)
        self.assertIn("Описание отсутствует", text)
        movie.overview = "🎬" * 10000
        self.assertLessEqual(len(format_movie_card(movie).encode("utf-16-le")) // 2, 4096)

    def test_selection_buttons_use_movie_id(self):
        from bot.keyboards import movie_selection_keyboard
        keyboard = movie_selection_keyboard([{"id": 157336, "title": "Фильм"}])
        self.assertEqual(keyboard.inline_keyboard[0][0].callback_data, "movie::157336")
