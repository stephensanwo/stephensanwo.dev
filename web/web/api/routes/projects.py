from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from web.types.context import WebMicroserviceContext
from web.api.dependencies import get_context
from web.types.pages import (Page)
from web.types.routes import Routes
from web.utils.data_parser import get_page_url, fetch_page_data


router = APIRouter()


@router.get(f"/{Routes.projects}", response_class=HTMLResponse)
async def projects(request: Request,
                   ctx: WebMicroserviceContext = Depends(get_context)):

    url = get_page_url(dir="web/pages/projects", page="index")
    page: Page = await fetch_page_data(url[1])
    page.request = request

    return ctx.templates.TemplateResponse(
        "page.html",
        page.dict())


@router.get("/projects/{project_slug}", response_class=HTMLResponse)
async def project(request: Request, project_slug: str,
                  ctx: WebMicroserviceContext = Depends(get_context)):

    url = get_page_url(dir="web/pages/projects",
                       page=f"{project_slug}")
    page: Page = await fetch_page_data(url[1])
    page.request = request

    return ctx.templates.TemplateResponse("page.html", page.dict())
