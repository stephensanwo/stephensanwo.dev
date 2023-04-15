from web.types.context import WebMicroserviceContext
from fastapi import Request
from typing import cast


def get_context(request: Request) -> WebMicroserviceContext:
    return cast(WebMicroserviceContext, request.app.state.context)
