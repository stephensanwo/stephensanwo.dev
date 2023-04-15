from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from web.types.context import WebMicroserviceContext
from web.types.pages import Page
from web.api.dependencies import get_context
from web.types.routes import Routes
from web.utils.data_parser import get_page_url, fetch_page_data

router = APIRouter()


@router.get(f"/{Routes.index}", response_class=HTMLResponse)
async def index(request: Request,
                ctx: WebMicroserviceContext = Depends(get_context)):
    url = get_page_url(dir="web/pages/www", page="index")
    page: Page = await fetch_page_data(url[1])
    page.request = request
    return ctx.templates.TemplateResponse("index.html", page.dict())


@router.get(f"/{Routes.profile}", response_class=HTMLResponse)
async def profile(request: Request,
                  ctx: WebMicroserviceContext = Depends(get_context)):
    url = get_page_url(dir="web/pages/www", page="profile")
    page: Page = await fetch_page_data(url[1])
    page.request = request
    return ctx.templates.TemplateResponse("profile.html", page.dict())


@router.get(f"/{Routes.ai_playground}", response_class=HTMLResponse)
async def playground(request: Request,
                     ctx: WebMicroserviceContext = Depends(get_context)):
    url = get_page_url(dir="web/pages", page="ai-playground")
    page: Page = await fetch_page_data(url[1])
    page.request = request
    return ctx.templates.TemplateResponse("profile.html", page.dict())
