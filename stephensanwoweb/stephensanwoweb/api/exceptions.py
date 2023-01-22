import os
from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.exceptions import HTTPException
from stephensanwoweb.types.context import WebMicroserviceContext
from fastapi.templating import Jinja2Templates
from stephensanwoweb.api.dependencies import get_context

async def not_found_error( request: Request, exc: HTTPException):
    ctx = get_context(request)
    return ctx.templates.TemplateResponse('404.html', {'request': request, "notification":False, "notification_message" : '', 
    "meta": {
        "title": "Page Not Found"
    },}, status_code=404)

async def unauthorized( request: Request, exc: HTTPException):
    ctx = get_context(request)
    return ctx.templates.TemplateResponse('401.html', {'request': request, "notification":False, "notification_message" : '', 
    "meta": {
        "title": "Unauthorized Access"
    },}, status_code=401)



async def internal_error(request: Request, exc: HTTPException):
    ctx = get_context(request)
    return ctx.templates.TemplateResponse('500.html', {'request': request, "notification":False, "notification_message" : '', 
    "meta": {
        "title": "Internal Server Error"
    },}, status_code=500)
    
exception_handlers = {
    401: unauthorized,
    404: not_found_error,
    500: internal_error
}

