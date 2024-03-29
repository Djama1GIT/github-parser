from datetime import date
from typing import List, Optional

from fastapi import APIRouter, Query, HTTPException
from fastapi.openapi.models import Example

from . import schemas
from .apiclient import fetch_top_repositories, fetch_repo_activity
from ..logger import logger

router = APIRouter(
    prefix="/api/repos",
    tags=["repositories"]
)


@router.get('/top100', response_model=List[schemas.Repository])
async def top100(
        sorting_method: Optional[str] = Query("stars", openapi_examples={
            "stars": Example(value="stars"),
            "forks": Example(value="forks"),
            "help wanted issues": Example(value="help-wanted-issues"),
            "updated": Example(value="updated"),
        })
):
    logger.info(f"Received request for top 100 repositories with sorting method: {sorting_method}")

    if sorting_method not in ["stars", "forks", "help-wanted-issues", "updated"]:
        logger.error(f"Invalid sorting method: {sorting_method}")
        raise HTTPException(status_code=422, detail="Incorrect sorting method")

    top = await fetch_top_repositories(sorting_method)
    return top


@router.get('/{owner}/{repo}/activity', response_model=List[schemas.RepoActivity])
async def repo_activity(owner: str, repo: str, since: date, until: date):
    logger.info(f"Received request for repository activity for {owner}/{repo} from {since} to {until}")
    activity = await fetch_repo_activity(owner, repo, since, until)
    return activity
