from pydantic import BaseModel
from web.types.frontend import FrontEnd
from web.types.server import (Server, Cors)
from web.types.metadata import (Metadata, Secrets)
from web.types.oauth import OauthSettings
from web.types.github import GithubSettings
from web.types.build import BuildConfig


class WebSettings(BaseModel):
    metadata: Metadata
    cors: Cors
    frontend: FrontEnd
    server: Server
    oauth_settings: dict[str, OauthSettings]
    secrets: Secrets
    github_settings: GithubSettings
    build_config: BuildConfig
