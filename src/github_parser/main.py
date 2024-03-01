from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

from pydantic import ValidationError

from redis import asyncio as aioredis

from .repos.router import router as repos_router

from .config import Settings
from .logger import logger

settings = Settings()

app = FastAPI(
    title=settings.NAME,
    version='1.0',
    contact={
        "name": "GitHub of the project",
        "url": "https://github.com/Djama1GIT/github-parser"
    },
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH"],
    allow_headers=["*"],
)

app.include_router(repos_router)


@app.exception_handler(ValidationError)
async def validation_exception_error(request: Request, exc: ValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({'detail': exc.errors()})
    )


@app.exception_handler(Exception)
async def internal_server_error(request: Request, exc: Exception):
    logger.error(exc)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=jsonable_encoder({'detail': "Internal Server Error"})
    )


@app.on_event("startup")
async def startup():
    redis = aioredis.from_url(f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}")
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
