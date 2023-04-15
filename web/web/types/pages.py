from pydantic import BaseModel
from fastapi import Request
from typing import Optional
from datetime import datetime


class MetaTags(BaseModel):
    product: str = ""
    title: str = ""
    description: str = ""
    type: str = ""
    url: str = ""
    image: str = ""
    tags: list[str] = []
    authors: list[str] = []


class Url(BaseModel):
    id: str
    url: str
    title: str


class Body(BaseModel):
    type: str = ""
    content: Optional[str] | Optional[list[str]]
    language: Optional[str]
    title: Optional[str]
    url: Optional[str]


class Cards(BaseModel):
    id: str = ""
    title: str = ""
    description: str = ""
    url: str = ""
    dateUpdated: str = ""
    coverImage: str = ""
    readTime: int = 1
    isInfographic: bool = False
    category: str = "SE"
    author: str = "Stephen Sanwo"


class Links(BaseModel):
    id: str = ""
    title: str = ""
    description: str = ""
    url: str = ""


class Data(BaseModel):
    title: str = ""
    urls: list[Url] = []
    caption: str = ""
    tags: list[str] = []
    body: list[Body] = []
    cards: list[Cards] = []
    links: list[Links] = []

    class Config:
        arbitrary_types_allowed = True


class BreadCrumb(BaseModel):
    page: str = ""
    page_url: str = ""


class Page(BaseModel):
    request: Optional[Request]
    title: str = ""
    slug: str = ""
    notification: bool = False
    notification_message: str = ""
    content: str = ""
    breadcrumb: list[BreadCrumb] = []
    meta: MetaTags = MetaTags()
    data: Data = Data()
    last_update: datetime = str(datetime.now())
    mins_read: int = 0
    extras: Optional[dict[str, (str | list | dict)]]

    class Config:
        arbitrary_types_allowed = True
