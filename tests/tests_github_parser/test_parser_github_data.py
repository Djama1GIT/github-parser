import json

import pytest
import requests
from requests.models import Response

from src.github_parser.parse_github_data import fetch_top_repositories, fetch_repo_activity

HOST = "http://51.250.2.103:8080"


@pytest.fixture
def mock_requests_get(requests_mock):
    def _mock_requests_get(url, json=json.dumps([]), status_code=200):
        mock_response = Response()
        mock_response.status_code = status_code
        mock_response._content = json.encode('utf-8')
        requests_mock.get(url, text=json)
        return mock_response

    return _mock_requests_get


def test_fetch_top_repositories_success(mock_requests_get):
    # Mock the successful response
    mock_data = []
    mock_requests_get(f"{HOST}/api/repos/top100?sorting_method=stars", json=json.dumps(mock_data))

    result = fetch_top_repositories("stars")
    assert result == mock_data


def test_fetch_top_repositories_error(mock_requests_get):
    # Mock the error response
    mock_requests_get(f"{HOST}/api/repos/top100?sorting_method=stars", status_code=404)

    result = fetch_top_repositories("stars")
    assert result == []


def test_fetch_repo_activity_success(mock_requests_get):
    # Mock the successful response
    mock_data = []
    mock_requests_get(f"{HOST}/api/repos/repo1/activity?since=2024-01-01&until=2024-03-01", json=json.dumps(mock_data))

    result = fetch_repo_activity("repo1", "2024-01-01", "2024-03-01")
    assert result == mock_data


def test_fetch_repo_activity_error(mock_requests_get):
    # Mock the error response
    mock_requests_get(f"{HOST}/api/repos/repo1/activity?since=2024-01-01&until=2024-03-01", status_code=404)

    result = fetch_repo_activity("repo1", "2024-01-01", "2024-03-01")
    assert result == []
