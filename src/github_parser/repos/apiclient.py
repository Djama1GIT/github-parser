import requests
from typing import List

from fastapi_cache.decorator import cache

from . import schemas
from ..logger import logger


@cache(expire=3600)
def fetch_repositories(sort_method: str = "stars") -> List[schemas.Repository]:
    logger.info("fetch")
    url = f"https://api.github.com/search/repositories?q={sort_method}:%3E1&sort={sort_method}&per_page=100"
    response = requests.get(url)
    data = response.json()

    if response.status_code != 200:
        raise Exception(f"Request failed with status code {response.status_code}")

    repositories = [
        schemas.Repository(
            repo=repository["full_name"],
            owner=repository["owner"]["login"],
            position_cur=idx,
            position_prev=idx + 1,
            stars=repository["stargazers_count"],
            watchers=repository["watchers_count"],
            forks=repository["forks_count"],
            open_issues=repository["open_issues_count"],
            language=repository["language"]
        )
        for idx, repository in enumerate(data["items"])
    ]

    return repositories
