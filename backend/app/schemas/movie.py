from pydantic import BaseModel


class MovieCard(BaseModel):
    id: int
    title: str
    overview: str
    release_date: str | None = None
    vote_average: float
    poster_url: str | None = None


class MovieSearchResponse(BaseModel):
    page: int
    total_pages: int
    total_results: int
    results: list[MovieCard]


class MovieDetail(MovieCard):
    genres: list[str]
    runtime: int | None = None
