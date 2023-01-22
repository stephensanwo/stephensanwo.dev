import os
from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from stephensanwoweb.types.context import WebMicroserviceContext
from stephensanwoweb.api.dependencies import get_context
from stephensanwoweb.data import parse_data
from stephensanwoweb.types.routes import Routes

router = APIRouter()

@router.get(f"/{Routes.ai_playground}", response_class=HTMLResponse)
async def ai_playground(request: Request, ctx: WebMicroserviceContext = Depends(get_context)):
    return ctx.templates.TemplateResponse("page.html", parse_data(request, Routes.ai_playground))
