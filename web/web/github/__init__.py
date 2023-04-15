from github import Github
from pydantic import BaseModel
import uuid
from web.types.github import GithubSettings


class GithubClient(BaseModel):
    github_settings: GithubSettings

    @property
    def repo(self):
        try:
            return Github(
                self.github_settings.personal_access_token).get_repo(
                    self.github_settings.blog_repo)
        except Exception:
            pass

    @property
    def repo_files(self):
        return self.repo.get_contents("")

    def create_file(self, data: str):
        file_id = uuid.uuid4()
        self.repo.create_file(
            f"{file_id}.yml",
            "new post", data,
            branch="main")
        return file_id

    def get_repo_file(self, file_id: str):
        return self.repo.get_contents(f"{file_id}.yml")

    def delete_file(self, file_id: str):
        contents = self.repo.get_contents(f"{file_id}.yml", ref="main")
        self.repo.delete_file(
            contents.path,
            "remove post",
            contents.sha,
            branch="main")
        return file_id

    class Config:
        arbitrary_types_allowed = True
