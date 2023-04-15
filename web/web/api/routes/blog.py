from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from web.types.context import WebMicroserviceContext
from web.api.dependencies import get_context
from web.types.pages import (Page, Cards)
import markdown
import math
from web.types.routes import Routes
from web.utils.data_parser import (
    fetch_page_data, get_page_urls, get_page_url)
import os

router = APIRouter()


@router.get(f"/{Routes.blog}", response_class=HTMLResponse)
async def blog_list(
        request: Request,
        ctx: WebMicroserviceContext = Depends(get_context)):

    urls = get_page_urls(dir="web/pages/",
                         page="blog", include_subdirectories=True)
    cards: list[Cards] = []

    # TODO: Handle pagination
    for url in urls[:9]:
        page = await fetch_page_data(url[1])
        cards.append(
            Cards(
                id=f"/blog/{url[0]}",
                title=page.title,
                description=page.data.caption,
                url=f"/blog/{url[0]}",
                dateUpdated=page.last_update.split(" ")[0],
                coverImage=page.meta.image,
                readTime=math.ceil(
                    len(page.data.body[0].content) / (250 * 4.7)),
                isInfographic=True if page.meta.product == "Infographics"
                else False,
                category=f"{page.data.tags[0]}",
                author=page.meta.authors[0]
            ).dict()
        )

    # Build blog list page
    ROOT = os.path.dirname(os.path.abspath("./web"))
    blog_path = os.path.join(ROOT, "web/pages/blog.yml")
    blog_list_page: Page = await fetch_page_data(blog_path)

    blog_list_page.data.cards = list(reversed(cards))
    blog_list_page.request = request
    return ctx.templates.TemplateResponse("page.html", blog_list_page.dict())


@router.get("/blog/{blog_slug}", response_class=HTMLResponse)
async def blog_slug(request: Request,
                    blog_slug: str,
                    ctx: WebMicroserviceContext = Depends(get_context)):

    url = get_page_url(dir="web/pages/blog", page=f"{blog_slug}")
    page: Page = await fetch_page_data(url[1])
    page.request = request
    try:
        for body in page.data.body:
            body.content = markdown.markdown(
                body.content, extensions=['fenced_code'])
    except Exception:
        pass

    return ctx.templates.TemplateResponse("page.html", page.dict())


@router.get("/blog/{blog_category}/{blog_slug}", response_class=HTMLResponse)
async def blog_category_slug(
        request: Request,
        blog_category: str,
        blog_slug: str,
        ctx: WebMicroserviceContext = Depends(get_context)):

    # Route for blog items with categories

    url = get_page_url(
        dir=f"web/pages/blog/{blog_category}", page=f"{blog_slug}")
    page: Page = await fetch_page_data(url[1])
    page.request = request
    try:
        for body in page.data.body:
            body.content = markdown.markdown(
                body.content, extensions=['fenced_code'])
    except Exception:
        pass

    return ctx.templates.TemplateResponse("page.html", page.dict())
