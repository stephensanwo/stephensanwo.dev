from fastapi import APIRouter, Depends, Request
from starlette.responses import HTMLResponse, RedirectResponse
from stephensanwoweb.types.context import WebMicroserviceContext
from stephensanwoweb.api.dependencies import get_context
from stephensanwoweb.types.pages import (MetaTags, Page, Data, Url, Links, BreadCrumb)
from stephensanwoweb.data import parse_data
from stephensanwoweb.github import GithubClient
import base64
import yaml
from stephensanwoweb.data.blog_index import blog_index_data
from typing import Optional
import math
from stephensanwoweb.types.routes import BackendRoutes

router = APIRouter()

@router.get(f'/{BackendRoutes.dashboard}')
async def dashboard(request: Request, ctx: WebMicroserviceContext = Depends(get_context)):
    app_url = request.url_for("index")
    return ctx.templates.TemplateResponse("page.html", parse_data(request, BackendRoutes.dashboard))

@router.get(f'/{BackendRoutes.blog}')
async def blog(request: Request, force_refresh : Optional[bool] = False ,ctx: WebMicroserviceContext = Depends(get_context)):
    cache = await ctx.cache.get_cache_data(key="blog_backend")
    if cache == None or force_refresh == True:
        app_url = request.url_for("index")    
        links = []
        for index, file in enumerate(ctx.github_client.repo_files):
            title = file.name
            file_id = file.name.split('.yml')[0]
            try:
                title = (base64.b64decode(file.content).decode('utf-8')).split('slug:')[0].split('title:')[1]
            except:
                pass
            links.append(
                Links(
                    id = index,
                        title= title,
                        description=f"File: {file.name} <br/> Url: {file.html_url} <br/> SHA: {file.sha}",
                        # description = html ,
                        status= "",
                        url= file.html_url,
                        actions = f"<a href ='{app_url}dashboard/blog/publish?file_id={file_id}'>Publish</a> | <a href ='{app_url}dashboard/blog/unpublish?file_id={file_id}'>Unublish</a> | <a href ='{app_url}dashboard/blog/delete?file_id={file_id}'>Delete</a>"
                    ),
            )
        blog_list = parse_data(request, "dashboard_blog", True)
        blog_list.data.links = links
        
        # Cache data
        await ctx.cache.store_cache_data(cache_timeout=360, key="blog_backend", value=blog_list.dict(exclude={"request"}))
        return ctx.templates.TemplateResponse("page.html", blog_list.dict())
    else:
        blog_list = Page(**cache)
        blog_list.request = request
        return ctx.templates.TemplateResponse("page.html", blog_list.dict())

@router.get(f'/{BackendRoutes.create_blog}')
async def create(request: Request, ctx: WebMicroserviceContext = Depends(get_context)):
    app_url = request.url_for("index")
    file_id = ctx.github_client.create_file(data = blog_index_data)
    return RedirectResponse(f"{ctx.settings.github_settings.github_archive_url}/{file_id}.yml")

@router.get(f'/{BackendRoutes.publish_blog}')
async def publish(request: Request, file_id: str ,ctx: WebMicroserviceContext = Depends(get_context)):
    raw = ctx.github_client.get_repo_file(file_id)
    yaml_data = yaml.safe_load(base64.b64decode(raw.content).decode('utf-8'))
    data: Page = Page.parse_obj(yaml_data)
    try:
        data.mins_read = math.ceil(len(data.data.body[0].content)/ (250 * 4.7))
    except:
        # Account for posts without markdown content
        pass
    await ctx.cache.store_json(key = "blog_data", data=data.dict(), path=f".{data.slug}")
    return RedirectResponse(f"/{BackendRoutes.blog}")

@router.get(f'/{BackendRoutes.delete_blog}')
async def delete(request: Request, file_id: str ,ctx: WebMicroserviceContext = Depends(get_context)):
    raw = ctx.github_client.get_repo_file(file_id)
    yaml_data = yaml.safe_load(base64.b64decode(raw.content).decode('utf-8'))
    data: Page = Page.parse_obj(yaml_data)
    await ctx.cache.delete_json(key = "blog_data", path = data.slug)
    ctx.github_client.delete_file(file_id)
    return RedirectResponse(f"/{BackendRoutes.blog}?force_refresh=True")

@router.get(f'/{BackendRoutes.unpublish_blog}')
async def unpublish(request: Request, file_id: str ,ctx: WebMicroserviceContext = Depends(get_context)):
    raw = ctx.github_client.get_repo_file(file_id)
    yaml_data = yaml.safe_load(base64.b64decode(raw.content).decode('utf-8'))
    data: Page = Page.parse_obj(yaml_data)
    await ctx.cache.delete_json(key = "blog_data", path = data.slug)
    return RedirectResponse(f"/{BackendRoutes.blog}?force_refresh=True")