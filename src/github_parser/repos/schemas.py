from datetime import date, datetime
from typing import List, Optional

from pydantic import Field, BaseModel


class Repository(BaseModel):
    repo: str = Field(..., description="Repository name (full_name in the GitHub API)")
    owner: str = Field(..., description="repository")
    position_cur: int = Field(..., description="current position in the top")
    position_prev: int = Field(..., description="previous position in the top")
    stars: int = Field(..., description="number of stars")
    watchers: int = Field(..., description="number of views")
    forks: int = Field(..., description="number of forks")
    open_issues: int = Field(..., description="number of open issues")
    language: Optional[str] = Field(..., description="language")


class RepoActivity(BaseModel):
    date: datetime = Field(..., description="date")
    commits: int = Field(..., description="Number of commits for a specific day")
    authors: List[str] = Field(..., description="List of developers who performed commits")
