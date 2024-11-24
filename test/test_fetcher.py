import os
import pytest
import requests_mock
from dotenv import load_dotenv
from src.github.fetcher import GithubCommentFetcher

load_dotenv()

@pytest.fixture
def github_token():
    return os.getenv("GITHUB_PAT")

def test_parse_comment_url(github_token):
    comment_url = "https://github.com/swellful-life/blogspot/issues/1#issuecomment-2495499151"
    owner, repo, issue_number, comment_id = GithubCommentFetcher(github_token).parse_comment_url(comment_url)
    assert owner == "swellful-life"
    assert repo == "blogspot"
    assert issue_number == 1
    assert comment_id == 2495499151

def test_fetch_comment(github_token, requests_mock):
    api_url = "https://api.github.com/repos/swellful-life/blogspot/issues/comments/2495499151"
    mock_response = {
        "id": 1,
        "body": "hello, world!"
    }

    requests_mock.get(api_url, json=mock_response)

    fetcher = GithubCommentFetcher(github_token)
    comment = fetcher.fetch_comment("swellful-life", "blogspot", 2495499151)

    assert comment["body"] == "hello, world!"