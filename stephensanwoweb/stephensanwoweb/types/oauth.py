from pydantic import BaseModel, validator
from enum import Enum

class OauthProviders(str, Enum):
    github = "github"

class OauthSettings(BaseModel):
    type: str = OauthProviders.github.value
    client_id: str = ""
    client_secret: str = ""
    access_token_url : str = ""
    authorize_url: str = ""
    redirect_uri: str = ""
    api_base_url: str = ""
