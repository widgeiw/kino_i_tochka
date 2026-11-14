from fastapi import FastAPI

from .routers.movies import router as movies_router

app = FastAPI(title="Кино и точка API", version="0.1.0")


@app.get("/health", tags=["System"])
async def health_check():
    return {"status": "ok"}


app.include_router(movies_router, prefix="/api/v1")
