from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class Repository(BaseModel):
    repo: str = Field(..., description="repository name (full_name in the GitHub API)", example="hello-world")
    owner: str = Field(..., description="repository", example="octocat")
    position_cur: int = Field(..., description="current position in the top", example=1)
    position_prev: int = Field(..., description="previous position in the top", example=2)
    stars: int = Field(..., description="number of stars", example=777)
    watchers: int = Field(..., description="number of views", example=200)
    forks: int = Field(..., description="number of forks", example=300)
    open_issues: int = Field(..., description="number of open issues", example=400)
    language: Optional[str] = Field(None, description="language", example="Python")


class RepoActivity(BaseModel):
    date: datetime = Field(..., description="date", example="2024-03-01")
    commits: int = Field(..., description="number of commits for a specific day", example=5)
    authors: List[str] = Field(..., description="list of developers who performed commits", example=["octocat"])
