import datetime

import pytest

from src.github_api_app.repos import schemas
from src.github_api_app.repos.apiclient import serialize_repositories, fetch_top_repositories, \
    serialize_commits_data_order_by_date, fetch_repo_activity


@pytest.mark.parametrize(
    "data, result",
    [
        (
                {
                    'total_count': 8498461,
                    'incomplete_results': False,
                    "items": [
                        {
                            'name': 'hugo',
                            'full_name': 'gohugoio/hugo',
                            'private': False,
                            'owner': {
                                'login': 'gohugoio',
                            },
                            'stargazers_count': 71557,
                            'watchers_count': 71557,
                            'language': 'Go',
                            'forks_count': 7254,
                            'open_issues_count': 494,
                            'forks': 7254,
                            'open_issues': 494,
                            'watchers': 71557,
                        }
                    ]
                },
                [schemas.Repository(
                    repo="gohugoio/hugo",
                    owner="gohugoio",
                    position_cur=0,
                    position_prev=1,
                    stars=71557,
                    watchers=71557,
                    forks=7254,
                    open_issues=494,
                    language="Go"
                )]
        ),
        (
                {},
                KeyError
        )
    ]
)
@pytest.mark.asyncio
async def test_serialize_repositories(data, result):
    if result is KeyError:
        with pytest.raises(KeyError):
            serialize_repositories(data)
    else:
        assert serialize_repositories(data) == result


@pytest.mark.parametrize(
    "sorting_method, per_page, result",
    [
        (
                "stars",
                1,
                [
                    schemas.Repository(
                        repo='freeCodeCamp/freeCodeCamp',
                        owner='freeCodeCamp',
                        position_cur=0,
                        position_prev=1,
                        stars=0,
                        watchers=0,
                        forks=0,
                        open_issues=0,
                        language='TypeScript'
                    )
                ]
        ),
    ]
)
@pytest.mark.asyncio
async def test_fetch_top_repositories(sorting_method, per_page, result):
    fetch = await fetch_top_repositories(sorting_method, per_page)
    for i in range(len(fetch)):
        fetch[i].stars = 0
        fetch[i].watchers = 0
        fetch[i].forks = 0
        fetch[i].open_issues = 0
    assert fetch == result


@pytest.mark.parametrize(
    "data, result",
    [
        (
                [
                    {
                        "sha": "4e74bb27434f0980c52e09fc42bc73073736336b",
                        "node_id": "C_kwDOHEdk59oAKDRlNzRiYjI3NDM0ZjA5ODBjNTJlMDlmYzQyYmM3MzA3MzczNjMzNmI",
                        "commit": {
                            "author": {
                                "name": "Djama1GIT",
                                "email": "dj.ama1@mail.ru",
                                "date": "2023-12-21T19:55:33Z"
                            },
                            "committer": {
                                "name": "Djama1GIT",
                                "email": "dj.ama1@mail.ru",
                                "date": "2023-12-21T19:55:33Z"
                            },
                            "message": "fix: fixed migrations and docker-compose\n1) added makemigrations to the server service in the docker-compose file\n2) added authorization check in product-details",
                            "tree": {
                                "sha": "5f41279f66a6bb22083b74b2bb8d8bf8acd86c12",
                                "url": "https://api.github.com/repos/Djama1GIT/red/git/trees/5f41279f66a6bb22083b74b2bb8d8bf8acd86c12"
                            },
                            "url": "https://api.github.com/repos/Djama1GIT/red/git/commits/4e74bb27434f0980c52e09fc42bc73073736336b",
                            "comment_count": 0,
                            "verification": {
                                "verified": False,
                                "reason": "unsigned",
                                "signature": None,
                                "payload": None
                            }
                        },
                        "url": "https://api.github.com/repos/Djama1GIT/red/commits/4e74bb27434f0980c52e09fc42bc73073736336b",
                        "html_url": "https://github.com/Djama1GIT/red/commit/4e74bb27434f0980c52e09fc42bc73073736336b",
                        "comments_url": "https://api.github.com/repos/Djama1GIT/red/commits/4e74bb27434f0980c52e09fc42bc73073736336b/comments",
                        "author": {
                            "login": "Djama1GIT",
                            "id": 89941580,
                            "node_id": "MDQ6VXNlcjg5OTQxNTgw",
                            "avatar_url": "https://avatars.githubusercontent.com/u/89941580?v=4",
                            "gravatar_id": "",
                            "url": "https://api.github.com/users/Djama1GIT",
                            "html_url": "https://github.com/Djama1GIT",
                            "followers_url": "https://api.github.com/users/Djama1GIT/followers",
                            "following_url": "https://api.github.com/users/Djama1GIT/following{/other_user}",
                            "gists_url": "https://api.github.com/users/Djama1GIT/gists{/gist_id}",
                            "starred_url": "https://api.github.com/users/Djama1GIT/starred{/owner}{/repo}",
                            "subscriptions_url": "https://api.github.com/users/Djama1GIT/subscriptions",
                            "organizations_url": "https://api.github.com/users/Djama1GIT/orgs",
                            "repos_url": "https://api.github.com/users/Djama1GIT/repos",
                            "events_url": "https://api.github.com/users/Djama1GIT/events{/privacy}",
                            "received_events_url": "https://api.github.com/users/Djama1GIT/received_events",
                            "type": "User",
                            "site_admin": False
                        },
                        "committer": {
                            "login": "Djama1GIT",
                            "id": 89941580,
                            "node_id": "MDQ6VXNlcjg5OTQxNTgw",
                            "avatar_url": "https://avatars.githubusercontent.com/u/89941580?v=4",
                            "gravatar_id": "",
                            "url": "https://api.github.com/users/Djama1GIT",
                            "html_url": "https://github.com/Djama1GIT",
                            "followers_url": "https://api.github.com/users/Djama1GIT/followers",
                            "following_url": "https://api.github.com/users/Djama1GIT/following{/other_user}",
                            "gists_url": "https://api.github.com/users/Djama1GIT/gists{/gist_id}",
                            "starred_url": "https://api.github.com/users/Djama1GIT/starred{/owner}{/repo}",
                            "subscriptions_url": "https://api.github.com/users/Djama1GIT/subscriptions",
                            "organizations_url": "https://api.github.com/users/Djama1GIT/orgs",
                            "repos_url": "https://api.github.com/users/Djama1GIT/repos",
                            "events_url": "https://api.github.com/users/Djama1GIT/events{/privacy}",
                            "received_events_url": "https://api.github.com/users/Djama1GIT/received_events",
                            "type": "User",
                            "site_admin": False
                        },
                        "parents": [
                            {
                                "sha": "8291dc2e9b0f48b48f272f2963df9bcbd28e8916",
                                "url": "https://api.github.com/repos/Djama1GIT/red/commits/8291dc2e9b0f48b48f272f2963df9bcbd28e8916",
                                "html_url": "https://github.com/Djama1GIT/red/commit/8291dc2e9b0f48b48f272f2963df9bcbd28e8916"
                            }
                        ]
                    }
                ],
                [
                    schemas.RepoActivity(
                        date=datetime.datetime(2023, 12, 21, 0, 0),
                        commits=1,
                        authors=['Djama1GIT']
                    )
                ]
        ),
        (
                {},
                []
        )
    ])
@pytest.mark.asyncio
async def test_serialize_commits_data_order_by_date(data, result):
    assert serialize_commits_data_order_by_date(data) == result


@pytest.mark.parametrize(
    "owner, repo, since, until, result",
    [
        (
                "Djama1GIT",
                "red",
                "2023-12-21",
                "2023-12-22",
                [
                    schemas.RepoActivity(
                        date=datetime.datetime(2023, 12, 21, 0, 0),
                        commits=1,
                        authors=['Djama1GIT']
                    )
                ]
        ),
        (
                "Djama1GIT",
                "red",
                "2023-12-21",
                "2023-12-21",
                []
        ),
    ]
)
@pytest.mark.asyncio
async def test_fetch_repo_activity(owner, repo, since, until, result):
    fetch = await fetch_repo_activity(owner, repo, since, until)
    assert fetch == result
