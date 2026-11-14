from fastapi.testclient import TestClient

from backend.app.main import app
import backend.app.routers.movies as movie_routes

client = TestClient(app)


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_search_query_is_required():
    response = client.get("/api/v1/movies/search")
    assert response.status_code == 422


def test_search_movies(monkeypatch):
    async def fake_tmdb_get(path, params):
        assert path == "/search/movie"
        assert params["query"] == "Интерстеллар"
        return {
            "page": 1,
            "total_pages": 1,
            "total_results": 1,
            "results": [{
                "id": 157336,
                "title": "Интерстеллар",
                "overview": "Описание фильма",
                "release_date": "2014-11-05",
                "vote_average": 8.4,
                "poster_path": "/poster.jpg",
            }],
        }

    monkeypatch.setattr(movie_routes, "tmdb_get", fake_tmdb_get)
    response = client.get("/api/v1/movies/search", params={"query": "Интерстеллар"})
    assert response.status_code == 200
    assert response.json()["results"][0]["id"] == 157336
    assert response.json()["results"][0]["poster_url"] == "https://image.tmdb.org/t/p/w500/poster.jpg"


def test_movie_details(monkeypatch):
    async def fake_tmdb_get(path, params):
        assert path == "/movie/157336"
        return {
            "id": 157336,
            "title": "Интерстеллар",
            "overview": "Описание фильма",
            "release_date": "2014-11-05",
            "vote_average": 8.4,
            "poster_path": None,
            "genres": [{"id": 878, "name": "Фантастика"}],
            "runtime": 169,
        }

    monkeypatch.setattr(movie_routes, "tmdb_get", fake_tmdb_get)
    response = client.get("/api/v1/movies/157336")
    assert response.status_code == 200
    assert response.json()["genres"] == ["Фантастика"]
    assert response.json()["runtime"] == 169
