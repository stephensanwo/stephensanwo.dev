from pydantic import BaseModel, validator
from .frontend import FrontEnd
from .server import (Server, Cors)
from .metadata import (Metadata, Environment, Secrets)
from .cache import RedisSettings
from .oauth import OauthSettings
from .github import GithubSettings


class WebSettings(BaseModel):
    metadata: Metadata(environment = Environment.dev)
    cors: Cors 
    frontend:  dict[str, FrontEnd]
    server: dict[str, Server]
    redis_settings: RedisSettings
    oauth_settings: OauthSettings
    secrets: Secrets
    github_settings: GithubSettings
    
    @validator('server')
    def validate_server(cls, value):
        for env in value.keys():
            if env not in [env.value for env in Environment]:
                raise ValueError("Invalid environment")
        return value
    



