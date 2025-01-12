from src.github.fetcher import GithubCommentFetcher
from src.formatter.formatter import CommentFormatter
from src.blogger.poster import BloggerPoster

# 1. GitHub 댓글 가져오기
fetcher = GithubCommentFetcher(github_token="your_github_token")
owner, repo, comment_id = fetcher.parse_comment_url("https://github.com/owner/repo/issues/1#issuecomment-12345")
comment_data = fetcher.fetch_comment(owner, repo, comment_id)

# 2. 댓글 내용 가공 및 HTML 변환
formatter = CommentFormatter()
html_content = formatter.markdown_to_html(comment_data["body"])
cleaned_html = formatter.clean_html(html_content)

# 3. Blogger에 포스팅
poster = BloggerPoster(
    client_id="your_client_id",
    client_secret="your_client_secret",
    refresh_token="your_refresh_token",
    blog_id="your_blog_id",
)
poster.post_to_blogger(
    title=f"GitHub Comment by {comment_data['user']['login']}",
    content=cleaned_html,
)