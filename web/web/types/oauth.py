from pydantic import BaseModel
from enum import Enum


class OauthProviders(str, Enum):
    github = "github"


class OauthSettings(BaseModel):
    type: str = None
    client_id: str = None
    client_secret: str = None
    access_token_url: str = None
    authorize_url: str = None
    redirect_uri: str = None
    api_base_url: str = None
