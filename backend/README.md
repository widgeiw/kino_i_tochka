# Backend — «Кино и точка» (первый этап)

Python 3.10+ needed. All commands are run from the repository root in Windows CMD.

```bat
py -m venv .venv
.venv\Scripts\activate
python -m pip install -r backend\requirements.txt
copy backend\.env.example backend\.env
```

Open `backend/.env` and replace the placeholder with your TMDB **API Read Access Token**.
Never commit `backend/.env` to GitHub.

Run the server:

```bat
python -m uvicorn backend.app.main:app --reload
```

Try http://127.0.0.1:8000/docs and http://127.0.0.1:8000/health.

```text
GET /api/v1/movies/search?query=Интерстеллар&page=1
GET /api/v1/movies/157336
```

Tests (do not need a TMDB token):

```bat
python -m pytest tests/test_backend.py -q
```
