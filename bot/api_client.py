"""Асинхронный доступ бота к FastAPI."""

import httpx


class BackendError(Exception):
    """Ошибка API с сообщением для пользователя."""


class MovieAPI:
    def __init__(self, client: httpx.AsyncClient):
        self.client = client

    async def search_movies(self, query: str, page: int = 1) -> dict:
        try:
            response = await self.client.get(
                "/api/v1/movies/search", params={"query": query, "page": page}
            )
            response.raise_for_status()
        except httpx.TimeoutException as exc:
            raise BackendError("Поиск занял слишком много времени. Попробуй ещё раз.") from exc
        except httpx.HTTPStatusError as exc:
            if exc.response.status_code == 422:
                text = "Проверь название: оно должно содержать от 1 до 100 символов."
            else:
                text = "Каталог фильмов временно недоступен. Попробуй позже."
            raise BackendError(text) from exc
        except httpx.RequestError as exc:
            raise BackendError("Не удалось связаться с сервером. Попробуй позже.") from exc
        try:
            data = response.json()
            if not isinstance(data, dict) or not isinstance(data.get("results"), list):
                raise ValueError("Invalid search response")
            for movie in data["results"]:
                if not isinstance(movie, dict) or not isinstance(movie.get("title"), str):
                    raise ValueError("Invalid movie")
            return data
        except (ValueError, TypeError) as exc:
            raise BackendError("Сервер вернул непонятный ответ. Попробуй позже.") from exc
