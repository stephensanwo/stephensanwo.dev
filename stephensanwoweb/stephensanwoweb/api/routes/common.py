import os
from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from stephensanwoweb.types.context import WebMicroserviceContext
from stephensanwoweb.api.dependencies import get_context
from stephensanwoweb.data import parse_data
from stephensanwoweb.types.routes import Routes

router = APIRouter()
        
@router.get(f"/{Routes.index}", response_class=HTMLResponse)
async def index(request: Request, ctx: WebMicroserviceContext = Depends(get_context)):
    return ctx.templates.TemplateResponse("index.html", parse_data(request, 'index'))

     
@router.get(f"/{Routes.profile}", response_class=HTMLResponse)
async def profile(request: Request, ctx: WebMicroserviceContext = Depends(get_context)):
    return ctx.templates.TemplateResponse("profile.html", {"request": request, "notification":False, "notification_message" : '', 
        "meta": {
        "title": "Stephen Sanwo's Profile",
        "product": "Profile"
    },
    "data": {
        "about_me": "I am a Fullstack Software, and Artificial Intelligence Solutions Engineer. I focus on architecting data-driven software that solve domain problems in complex data-oriented environments, and specific user cases in financial services, and retail. Currently, I am a software engineering manager with Accenture UK, and prior to that, I lead an analytics solutions development team at KPMG Nigeria, where I focused on developing and maintaining scalable analytics software solutions some of which includs KPMG’s ATM Reconciliation Application for Banks and KPMG’s Asset Reconciliation Solution.",
        "work_history" : [
            {
                "title": "Incoming Software Engineering Manager - Infinity Works, part of Accenture UK",
                "period": "Janurary 2023"

            }, {
                "title": "Manager & Technical Lead - KPMG Nigeria",
                "period": "September 2015 - October 2022"
            }
            , {
                "title": "Open Source Software and AI Engineer & Technical Writer (Github, FreeCodeCamp)",
                "period": "January 2020 - Current"
            }
        ],

        "competence": [
            "Data-driven Software", "Language Models", "Deep Learning", "Microservices", "Software Architecture", "User Interface Design", "Web and Mobile UI Development", "Software Systems Design", "Distributed Software", "REST APIs", "Event-driven Software", "Transformers"
        ],

        "stack": [
            "Python", "JavaScript", "TypeScript", "Golang", "SQL", "HTML5", "CSS", "FastAPI", "Flask", "NodeJs", "Net/HTTP", "Pytourch", "Tensorflow", "ReactJs", "React Native", "PostgreSQL", "MongoDB", "Redis", "DynamoDB", "Kafka", "Hadoop", "Spark", "AWS", "Linux", "Docker", "Kubernetes", "Git", "Github",  "Github Actions", "Nginx" 
        ]
    } })
