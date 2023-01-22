from pydantic import BaseModel

class GithubSettings(BaseModel):
    personal_access_token: str
    blog_repo: str
    github_archive_url: str