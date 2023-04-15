from web.types.settings import WebSettings
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from authlib.integrations.starlette_client import OAuth
from web.types.oauth import OauthProviders
from web.github import GithubClient


class WebMicroserviceContext(BaseModel):
    settings: WebSettings
    templates: Jinja2Templates = Jinja2Templates(directory="static/html")
    _oauth: OAuth = OAuth()

    @property
    def github_client(self):
        return GithubClient(github_settings=self.settings.github_settings)

    @property
    def oauth(self):
        self._oauth.register(
            name=OauthProviders.github.value,
            client_id=self.settings.oauth_settings.client_id,
            client_secret=self.settings.oauth_settings.client_secret,
            access_token_url=self.settings.oauth_settings.access_token_url,
            access_token_params=None,
            authorize_url=self.settings.oauth_settings.authorize_url,
            authorize_params=None,
            api_base_url=self.settings.oauth_settings.api_base_url,
            client_kwargs={'scope': 'user:email'},
        )

        return self._oauth

    class Config:
        arbitrary_types_allowed = True
