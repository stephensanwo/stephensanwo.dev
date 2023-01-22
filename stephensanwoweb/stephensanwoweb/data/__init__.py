from fastapi import Request
from stephensanwoweb.types.routes import Routes
import yaml
from stephensanwoweb.types.pages import (Page)
import markdown
import os
from typing import Optional

def parse_data(request: Request, path: str, object_response: Optional[bool] = False):
    ROOT = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(ROOT, f"./{path}.yml")
    with open(path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
    page = Page.parse_obj(config)
    page.request = request

    try:
        for body in page.data.body:
            body.content = markdown.markdown(body.content, extensions=['fenced_code'])
    except:
        pass

    if not object_response:
        return page.dict()

    else:
        return page

