import yaml
from web.types.pages import (Page)
import markdown
import os

ROOT = os.path.dirname(os.path.abspath("./web"))


def get_page_url(dir: str, page: str) -> str:
    path = os.path.join(ROOT, dir, f"{page}.yml")
    return (page, path)


def get_page_urls(dir: str,
                  include_subdirectories: bool) -> list[tuple]:
    path = os.path.join(ROOT, dir)
    urls = []

    if include_subdirectories:
        for root, dirs, files in os.walk(path):
            for file in files:
                filename = file.split(".yml")[0]
                relative_path = os.path.relpath(
                    root, os.path.join(ROOT, "web", "pages"))
                urls.append((filename, relative_path))

    else:
        for file in os.listdir(path):
            filename = file.split(".yml")[0]
            file_loc = os.path.join(path, file)

            if os.path.isfile(file_loc):
                urls.append((filename, filename))

    return urls


async def fetch_page_data(file_loc: str) -> Page:
    with open(file_loc, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
        page = Page.parse_obj(config)

        try:
            for body in page.data.body:
                body.content = markdown.markdown(
                    body.content, extensions=['fenced_code'])

        except Exception:
            pass

        return page
