from fastapi import Depends
# from sqlalchemy.ext.asyncio import AsyncSession # todo asyncpg session

from .repository import ReposRepository


# def get_repos_repository(get_async_session):
#     def _get_repos_repository(session: AsyncSession = Depends(get_async_session)) -> ReposRepository:
#         return ReposRepository(session)
#
#     return _get_repos_repository
