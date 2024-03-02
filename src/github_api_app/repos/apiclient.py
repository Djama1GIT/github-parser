from datetime import datetime, date

import requests
from typing import List

from fastapi_cache.decorator import cache

from . import schemas
from ..logger import logger
from ..config import Settings

settings = Settings()


def serialize_repositories(data: dict) -> List[schemas.Repository]:
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


@cache(expire=3600)
def fetch_top_repositories(sorting_method: str = "stars", per_page: int = 100) -> List[schemas.Repository]:
    logger.info(f"Fetch top repositories, "
                f"sorting method: {sorting_method}")

    url = f"https://api.github.com/search/repositories?" \
          f"q={sorting_method}:>1&" \
          f"sort={sorting_method}&" \
          f"per_page={per_page}&"
    headers = {'Accept': 'application/vnd.github.v3+json'}
    if settings.GITHUB_ACCESS_TOKEN:
        headers |= {
            'Authorization': f'token {settings.GITHUB_ACCESS_TOKEN}'
        }

    response = requests.get(url, headers)
    data = response.json()

    if response.status_code != 200:
        logger.error(f"An error has occurred while fetching top repositories, "
                     f"sorting method: {sorting_method}")
        logger.error(response.content)
        raise Exception(f"Request failed with status code {response.status_code}")

    repositories = serialize_repositories(data)

    return repositories


def serialize_commits_data_order_by_date(commits_data: List[dict]) -> List[schemas.RepoActivity]:
    activity = {}

    for commit in commits_data:
        commit_date = datetime.strptime(
            commit['commit']['author']['date'],
            "%Y-%m-%dT%H:%M:%SZ"
        )
        commit_date = commit_date.strftime("%Y-%m-%d")
        author = commit['commit']['author']['name']

        if commit_date not in activity:
            activity[commit_date] = schemas.RepoActivity(
                date=commit_date,
                commits=1,
                authors=[author],
            )
        else:
            activity[commit_date].commits += 1
            if author not in activity[commit_date].authors:
                activity[commit_date].authors.append(author)

    return list(activity.values())


@cache(expire=60)
def fetch_repo_activity(owner: str, repo: str, since: date,
                        until: date, per_page=9999) -> List[schemas.RepoActivity]:
    logger.info(f"Fetch repo activity, "
                f"owner: {owner}, "
                f"repo: {repo}, "
                f"since: {since}, "
                f"until: {until}")

    url = f"https://api.github.com/repos/{owner}/{repo}/commits?" \
          f"since={since}&" \
          f"until={until}&" \
          f"per_page={per_page}"
    headers = {'Accept': 'application/vnd.github.v3+json'}
    if settings.GITHUB_ACCESS_TOKEN:
        headers |= {
            'Authorization': f'token {settings.GITHUB_ACCESS_TOKEN}'
        }
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        logger.error(f"Error when executing the repo activity, "
                     f"owner: {owner}, "
                     f"repo: {repo}, "
                     f"since: {since}, "
                     f"until: {until}")
        logger.error(response.content)
        raise Exception(f"Error when executing the request: {response.status_code}")

    commits_data = response.json()
    activity_list = serialize_commits_data_order_by_date(commits_data)

    return activity_list
