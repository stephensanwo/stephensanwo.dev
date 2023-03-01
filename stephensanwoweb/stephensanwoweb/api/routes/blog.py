import os
from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from stephensanwoweb.types.context import WebMicroserviceContext
from stephensanwoweb.api.dependencies import get_context
from stephensanwoweb.types.pages import (Page, Cards)
import markdown
from stephensanwoweb.data import parse_data
from stephensanwoweb.types.routes import Routes

router = APIRouter()

@router.get(f"/{Routes.blog}", response_class=HTMLResponse)
async def projects(request: Request, ctx: WebMicroserviceContext = Depends(get_context)):
    
    blog_list = await ctx.cache.get_json(key="blog_data")
    cards: list[Cards] = []
    for key, blog in blog_list.items():
        cards.append(
            Cards(
                id = key,
                title = blog["title"],
                description = blog['data']["caption"],
                url = f"blog/{key}",
                dateUpdated = blog['last_update'].split(" ")[0],
                coverImage = blog['meta']['image'],
                readTime = blog['mins_read'],
                isInfographic = True if blog['meta']['product'] == "Infographics" else False,
                category = f"{blog['content'][:2]}".upper(),
                author = blog["meta"]["authors"][0]
            ).dict()
        )
    blog_page = parse_data(request, path="blog", object_response=True)
    blog_page.data.cards = list(reversed(cards))

    return ctx.templates.TemplateResponse("page.html", blog_page.dict())


@router.get("/blog/{blog_slug}", response_class=HTMLResponse)
async def projects(request: Request, blog_slug: str, ctx: WebMicroserviceContext = Depends(get_context)):
    cache = await ctx.cache.get_json(key="blog_data", path=blog_slug)
    blog = Page(**cache)
    blog.request = request

    try:
        for body in blog.data.body:
            body.content = markdown.markdown(body.content, extensions=['fenced_code'])
    except:
        pass
    return ctx.templates.TemplateResponse("page.html", blog.dict())

