"""Данные карточки из FastAPI и текст для Telegram."""

from pydantic import BaseModel, Field


class MovieDetail(BaseModel):
    id: int = Field(gt=0)
    title: str
    overview: str
    release_date: str | None = None
    vote_average: float
    poster_url: str | None = None
    genres: list[str]
    runtime: int | None = None


def format_movie_card(movie: MovieDetail) -> str:
    year = movie.release_date[:4] if movie.release_date else "год неизвестен"
    runtime = f"{movie.runtime} мин." if movie.runtime else "не указана"
    header = (
        f"🎬 {movie.title[:200]} ({year})\n"
        f"⭐ Рейтинг TMDB: {movie.vote_average:.1f}/10\n"
        f"🎭 Жанры: {', '.join(movie.genres)[:300] or 'не указаны'}\n"
        f"⏱ Продолжительность: {runtime}\n\n"
    )
    overview = movie.overview.strip() or "Описание отсутствует."
    # Запас к лимиту Telegram, в том числе для символов вне BMP.
    return header + (overview[:1200] + "…" if len(overview) > 1200 else overview)
