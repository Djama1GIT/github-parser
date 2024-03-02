import pytest

from tests.conftest import async_client as ac


@pytest.mark.parametrize(
    "sorting_method, status_code",
    [
        ("aboba", 422),
        ("stars", 200),
        ("forks", 200),
        ("updated", 200),
        ("help-wanted-issues", 200),
    ]
)
@pytest.mark.asyncio
async def test_top100(sorting_method, status_code):
    response = await ac.get(f"/api/repos/top100?sorting_method={sorting_method}")
    assert response.status_code == status_code


@pytest.mark.parametrize(
    "owner, repo, since, until, status_code, json",
    [
        (
                "Djama1GIT",
                "",
                "2023-12-21",
                "2023-12-21",
                404,
                {'detail': 'Not Found'}
        ),
        (
                "Djama1GIT",
                "red",
                "2023-12-21",
                "2023-12-21",
                200,
                []
        ),
        (
                "Djama1GIT",
                "red",
                "2023-12-21",
                "2023-12-22",
                200,
                [{'authors': ['Djama1GIT'], 'commits': 1, 'date': '2023-12-21T00:00:00'}]
        ),
    ]
)
@pytest.mark.asyncio
async def test_repo_activity(owner, repo, since, until, status_code, json):
    response = await ac.get(f"/api/repos/{owner}/{repo}/activity?since={since}&until={until}")
    assert response.status_code == status_code
    assert response.json() == json
