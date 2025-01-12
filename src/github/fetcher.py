from typing import Tuple
import re
import requests

class GithubCommentFetcher:
    def __init__(self, github_token: str):
        self.github_token = github_token

    def parse_comment_url(self, comment_url: str) -> Tuple[str, str, int, int]:
        """
        Parse the GitHub comment URL and return the owner, repo, issue number, and comment ID.
        Args:
            comment_url: The URL of the GitHub comment.
        Returns:
            A tuple of (owner, repo, issue_number, comment_id).
        Raises:
            ValueError: If the comment URL is invalid.
        """
        match = re.match(
            r"https://github\.com/(?P<owner>[^/]+)/(?P<repo>[^/]+)/issues/(?P<issue_number>\d+)#issuecomment-(?P<comment_id>\d+)",
            comment_url,
        )
        if not match:
            raise ValueError("Invalid GitHub comment URL format.")
        return match.group("owner"), match.group("repo"), int(match.group("issue_number")), int(match.group("comment_id"))

    def fetch_comment(self, owner: str, repo: str, comment_id: int) -> dict:
        url = f"https://api.github.com/repos/{owner}/{repo}/issues/comments/{comment_id}"
        headers = {"Authorization": f"token {self.github_token}"}
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to fetch GitHub comment: {response.json()}")
