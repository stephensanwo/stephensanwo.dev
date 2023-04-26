# flake8: noqa
import multiprocessing
from dotenv import load_dotenv
import os
from web.types.oauth import OauthSettings, OauthProviders
from web.types.metadata import Metadata, Environment, Secrets
from web.types.github import GithubSettings
from web.types.settings import WebSettings, Cors, FrontEnd
from web.types.server import Server
from web.types.build import BuildConfig, DomainObject
from cdk.types import CDKConfig

load_dotenv()

APP_ENVIRONMENT = os.environ.get("ENVIRONMENT")


def number_of_workers():
    return (multiprocessing.cpu_count() * 2) + 1


def settings() -> WebSettings:
    if APP_ENVIRONMENT == Environment.dev:
        return WebSettings(
            metadata=Metadata(
                environment=Environment.dev,
                version="0.0.1",
                path=""),

            cors=Cors(
                allow_origins=["*"],
            ),
            frontend=FrontEnd(
                is_notification=False,
                notification_message="",
            ),
            server=Server(
                host="127.0.0.1",
                port=4100,
                workers=number_of_workers(),
                reload=True,
                debug=True,
                ssl_keyfile="https/localhost+2-key.pem",
                ssl_certificate="https/localhost+2.pem",
            ),
            oauth_settings={
                OauthProviders.github: OauthSettings(
                    type=OauthProviders.github,
                    client_id=os.environ.get("GITHUB_CLIENT_ID"),
                    client_secret=os.environ.get("GITHUB_CLIENT_SECRET"),
                    access_token_url="https://github.com/lo\
                    gin/oauth/access_token",
                    authorize_url="https://github.com/login/oauth/authorize",
                    redirect_uri="https://127.0.0.1:4100/auth",
                    api_base_url="https://api.github.com/",
                )
            },
            secrets=Secrets(
                authlib_session_secret=os.environ.get(
                    "AUTHLIB_SESSION_SECRET"),
            ),
            github_settings=GithubSettings(
                personal_access_token=os.environ.get(
                    "GITHUB_PAT"),
                blog_repo="stephensanwo/stephensanwodev_blog_archive",
                github_archive_url="https://github.com/stephe\
                nsanwo/stephensanwodev_blog_archive/blob/main"
            ),
            build_config=BuildConfig(
                domains={
                    "www": DomainObject(
                        name="stephensanwo.dev",
                        domain="https://stephensanwo.dev",
                        redirects_object={
                            "www.stephensanwo.dev": "stephensanwo.dev"
                        },
                        static_dir="web/pages/www",
                        output_dir="dist/www",
                        xml_dir="dist/xml/www"

                    ),
                    "blog": DomainObject(
                        name="blog.stephensanwo.dev",
                        domain="https://blog.stephensanwo.dev",
                        redirects_object={
                        },
                        static_dir="web/pages/blog",
                        output_dir="dist/blog",
                        xml_dir="dist/xml/blog"
                    ),
                    "projects": DomainObject(
                        name="projects.stephensanwo.dev",
                        domain="https://projects.stephensanwo.dev",
                        redirects_object={
                        },
                        static_dir="web/pages/projects",
                        output_dir="dist/projects",
                        xml_dir="dist/xml/projects"
                    ),
                    "shared": DomainObject(
                        name="shared.stephensanwo.dev",
                        domain="https://sharded.stephensanwo.dev",
                        redirects_object={},
                        static_dir="web/pages/shared",
                        output_dir="dist/shared",
                    )
                }
            )
        )
    else:

        return None


def cdk_config() -> CDKConfig:
    return CDKConfig(
        account=os.environ.get("AWS_ACCOUNT"),
        region=os.environ.get("AWS_REGION"),
        description="Static site deploy for stephensanwo.dev",
        deployment_environment=os.environ.get("AWS_DEPLOYMENT_ENV"),
    )
