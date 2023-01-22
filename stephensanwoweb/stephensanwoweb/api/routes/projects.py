import os
from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from stephensanwoweb.types.context import WebMicroserviceContext
from stephensanwoweb.api.dependencies import get_context
from stephensanwoweb.types.pages import (MetaTags, Page, Data, Url, Links)
from stephensanwoweb.data import parse_data
from stephensanwoweb.types.routes import Routes

router = APIRouter()

@router.get(f"/{Routes.projects}", response_class=HTMLResponse)
async def projects(request: Request, ctx: WebMicroserviceContext = Depends(get_context)):
    return ctx.templates.TemplateResponse("page.html", parse_data(request, Routes.projects))

@router.get("/projects/{slug}", response_class=HTMLResponse)
async def project(request: Request, slug: str, ctx: WebMicroserviceContext = Depends(get_context)):
    return ctx.templates.TemplateResponse("page.html", parse_data(request, slug))
