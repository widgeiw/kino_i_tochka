from typing import Annotated

from fastapi import APIRouter, Path, Query

from ..schemas.movie import MovieCard, MovieDetail, MovieSearchResponse
from ..services.tmdb import tmdb_get

router = APIRouter(tags=["Movies"])


def to_movie_card(data: dict) -> dict:
    poster_path = data.get("poster_path")
    return {
        "id": data["id"],
        "title": data.get("title") or data.get("original_title") or "Без названия",
        "overview": data.get("overview") or "",
        "release_date": data.get("release_date") or None,
        "vote_average": data.get("vote_average") or 0.0,
        "poster_url": (
            f"https://image.tmdb.org/t/p/w500{poster_path}"
            if poster_path else None
        ),
    }


@router.get("/movies/search", response_model=MovieSearchResponse)
async def search_movies(
    query: Annotated[str, Query(min_length=1, max_length=100)],
    page: Annotated[int, Query(ge=1, le=500)] = 1,
):
    data = await tmdb_get(
        "/search/movie",
        params={
            "query": query,
            "page": page,
            "language": "ru-RU",
            "include_adult": False,
        },
    )
    return {
        "page": data["page"],
        "total_pages": data["total_pages"],
        "total_results": data["total_results"],
        "results": [to_movie_card(movie) for movie in data["results"]],
    }


@router.get("/movies/{movie_id}", response_model=MovieDetail)
async def movie_details(movie_id: Annotated[int, Path(gt=0)]):
    data = await tmdb_get(f"/movie/{movie_id}", params={"language": "ru-RU"})
    return {
        **to_movie_card(data),
        "genres": [genre["name"] for genre in data.get("genres", [])],
        "runtime": data.get("runtime"),
    }
