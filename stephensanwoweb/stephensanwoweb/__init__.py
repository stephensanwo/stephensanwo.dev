from typing import Optional
from structlog import get_logger
from stephensanwoweb.types.settings import WebSettings
from settings import settings
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from stephensanwoweb.api.routes import (ping, common, projects, ai_playground, blog, auth, backend)
from stephensanwoweb.api import exceptions
from fastapi.staticfiles import StaticFiles
from stephensanwoweb.types.context import WebMicroserviceContext
from stephensanwoweb.types.metadata import Environment
from starlette.middleware.sessions import SessionMiddleware

logger = get_logger(__name__)

class WebMicroservice:
    def __init__(self):
        self.settings: WebSettings = settings()
        self.api = FastAPI(title="Stephen Sanwo Web Microservice", version=self.settings.metadata.version, exception_handlers=exceptions.exception_handlers)
   
    @property
    def context(self) -> WebMicroserviceContext:
        return WebMicroserviceContext(settings = self.settings)

    def create_api(self):        
        self.api.state.settings = self.settings
        self.cors()
        self.configure_session(self.api)
        self.routes()
        self.mount_directories()
        self.application_context(self.api)
        return self.api

    def mount_directories(self):
        self.api.mount("/static", StaticFiles(directory="static"), name="static")

    def cors(self):        
        self.api.add_middleware(
            CORSMiddleware,
            allow_origins=self.settings.cors.allowed_origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    def configure_session(self, api: FastAPI):
        api.add_middleware(
            SessionMiddleware, secret_key=self.settings.secrets.authlib_session_secret)

    def routes(self):
        for router in [ping.router, common.router, projects.router, ai_playground.router, blog.router, auth.router, backend.router]:
            self.api.include_router(router, prefix =self.settings.metadata.path )

    def application_context(self, api: FastAPI):
        api.state.context = self.context
        
    

    
