"""Асинхронный доступ бота к FastAPI."""

import httpx


class BackendError(Exception):
    """Ошибка API с сообщением для пользователя."""


class MovieAPI:
    def __init__(self, client: httpx.AsyncClient):
        self.client = client

    async def _get(self, path: str, params: dict | None = None) -> httpx.Response:
        try:
            response = await self.client.get(path, params=params)
            response.raise_for_status()
        except httpx.TimeoutException as exc:
            raise BackendError("Сервер отвечает слишком долго. Попробуй ещё раз.") from exc
        except httpx.HTTPStatusError as exc:
            if exc.response.status_code == 404:
                text = "Фильм не найден. Попробуй выбрать другой."
            elif exc.response.status_code == 422:
                text = "Проверь название: оно должно содержать от 1 до 100 символов."
            else:
                text = "Каталог фильмов временно недоступен. Попробуй позже."
            raise BackendError(text) from exc
        except httpx.RequestError as exc:
            raise BackendError("Не удалось связаться с сервером. Попробуй позже.") from exc
        return response

    async def search_movies(self, query: str, page: int = 1) -> dict:
        response = await self._get("/api/v1/movies/search", {"query": query, "page": page})
        try:
            data = response.json()
            if not isinstance(data, dict) or not isinstance(data.get("results"), list):
                raise ValueError("Invalid search response")
            for movie in data["results"]:
                if (not isinstance(movie, dict)
                        or not isinstance(movie.get("title"), str)
                        or type(movie.get("id")) is not int or movie["id"] <= 0):
                    raise ValueError("Invalid movie")
            return data
        except (ValueError, TypeError) as exc:
            raise BackendError("Сервер вернул непонятный ответ. Попробуй позже.") from exc

    async def movie_details(self, movie_id: int):
        from bot.movie_card import MovieDetail
        from pydantic import ValidationError

        response = await self._get(f"/api/v1/movies/{movie_id}")
        try:
            return MovieDetail.model_validate(response.json())
        except (ValueError, ValidationError) as exc:
            raise BackendError("Сервер вернул непонятную карточку фильма. Попробуй позже.") from exc
