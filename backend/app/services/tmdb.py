import os
from pathlib import Path

import httpx
from dotenv import load_dotenv
from fastapi import HTTPException

# Read the secret from backend/.env when running locally.
load_dotenv(Path(__file__).resolve().parents[2] / ".env")

TMDB_BASE_URL = "https://api.themoviedb.org/3"


async def tmdb_get(path: str, params: dict | None = None) -> dict:
    token = os.getenv("TMDB_READ_ACCESS_TOKEN", "").strip()
    if not token or token == "put_your_read_access_token_here":
        raise HTTPException(status_code=503, detail="TMDB token is not configured")

    headers = {
        "Authorization": f"Bearer {token}",
        "accept": "application/json",
    }

    try:
        async with httpx.AsyncClient(timeout=8.0) as client:
            response = await client.get(
                f"{TMDB_BASE_URL}{path}",
                headers=headers,
                params=params,
            )
            response.raise_for_status()
            return response.json()
    except httpx.TimeoutException as exc:
        raise HTTPException(status_code=504, detail="TMDB did not respond in time") from exc
    except httpx.HTTPStatusError as exc:
        status = exc.response.status_code
        if status == 404:
            raise HTTPException(status_code=404, detail="Movie not found") from exc
        if status == 429:
            raise HTTPException(status_code=503, detail="TMDB rate limit exceeded") from exc
        raise HTTPException(status_code=502, detail="TMDB returned an error") from exc
    except httpx.RequestError as exc:
        raise HTTPException(status_code=502, detail="Unable to reach TMDB") from exc
