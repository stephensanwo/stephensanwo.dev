from pydantic import BaseModel


class GithubSettings(BaseModel):
    personal_access_token: str = None
    blog_repo: str = None
    github_archive_url: str = None
