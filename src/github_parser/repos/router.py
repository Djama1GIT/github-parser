# import datetime
# import re
from datetime import date, datetime
from typing import List

from fastapi import APIRouter

from . import schemas
from .apiclient import fetch_repositories
from ..logger import logger

# from fastapi.responses import JSONResponse, Response
#
# from db import get_async_session
# from utils.logger import logger
# from .dependencies import get_ref_repository
# from .repository import RefRepository

#
# from utils.utils import fastapi_users

router = APIRouter(
    prefix="/api/repos",
    tags=["repositories"]
)


@router.get('/top100', response_model=List[schemas.Repository])
async def top100():
    res = await fetch_repositories()
    logger
    return res


@router.get('{owner}/{repo}/activity', response_model=List[schemas.RepoActivity])
def repo_activity(owner: str, repo: str, since: date, until: date):
    return [schemas.RepoActivity(
        date=datetime(2024, 3, 1),
        commits=27,
        authors=["GADJIIAVOV", "DJAMAL"]
    ).__dict__]
