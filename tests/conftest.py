import os
import sys

import redis as aioredis
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi.testclient import TestClient
from httpx import AsyncClient

sys.path.insert(0, os.getcwd())
from src.github_api_app.main import app

redis = aioredis.from_url("redis://localhost:6379/2")
FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")

client = TestClient(app)
async_client = AsyncClient(app=app, base_url='http://test')