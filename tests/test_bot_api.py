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
            return httpx.Response(200, json={"results": [{"id": 1, "title": "Фильм"}]})
        data = await self.request_with(handler, "Интерстеллар & кино")
        self.assertEqual(data["results"][0]["id"], 1)

    async def test_empty_results(self):
        data = await self.request_with(lambda r: httpx.Response(200, json={"results": []}))
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
