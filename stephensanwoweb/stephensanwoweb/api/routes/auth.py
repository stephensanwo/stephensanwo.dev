from fastapi import APIRouter, Depends, Request
from starlette.responses import HTMLResponse, RedirectResponse
from authlib.integrations.starlette_client import OAuth, OAuthError
from stephensanwoweb.types.context import WebMicroserviceContext
from stephensanwoweb.api.dependencies import get_context
from stephensanwoweb.types.pages import (MetaTags)
from stephensanwoweb.types.routes import BackendRoutes

router = APIRouter()

@router.get(f'/{BackendRoutes.admin}')
async def admin(request: Request, ctx: WebMicroserviceContext = Depends(get_context)):
    app_url = request.url_for("index")
    return ctx.templates.TemplateResponse("auth_page.html", {"request": request, "meta" : MetaTags(
        product="Admin",
        title = "Admin | Stephen Sanwo",
        description = "Admin Page",  
        type = "website",
        url = f"{app_url}admin",
        image = "", 
        tags = ["Admin"],
        authors = ["Stephen Sanwo"]
        ),
    "oauth_url": "https://127.0.0.1:4100/login"
        })

@router.get(f'/{BackendRoutes.login}')
async def login(request: Request, ctx: WebMicroserviceContext = Depends(get_context)):
    return await ctx.oauth.github.authorize_redirect(request, ctx.settings.oauth_settings.redirect_uri)

@router.get(f'/{BackendRoutes.auth}')
async def authorize(request: Request, ctx: WebMicroserviceContext = Depends(get_context)):
    # try:
    token = await ctx.oauth.github.authorize_access_token(request)
    print(token)
    resp = await ctx.oauth.github.get('user', token=token)
    print(resp)
    # token = await ctx.oauth.github.authorize_access_token(request)
    # except OAuthError as error:
    #     return HTMLResponse(f'<h1>{error.error}</h1>')

    # resp = token.get('user', token)
    # print(resp)
    # # resp.raise_for_status()
    # profile = resp.json()
    # print(profile)
    # do something with the token and profile
    return RedirectResponse(url='/')
