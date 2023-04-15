from pydantic import BaseModel
from web.types.settings import WebSettings
from web.types.context import WebMicroserviceContext
from web.build.blog import build_blog_list
from web.build.pages import build_pages
from web.build.assets import build_assets
from web.build.projects import build_project_slug
from web.build.shared import build_shared
import os
import shutil
from config import settings


class StaticBuild(BaseModel):
    settings_: WebSettings = settings()
    urls: list[str] = []

    @property
    def context(self) -> WebMicroserviceContext:
        return WebMicroserviceContext(settings=self.settings_)

    async def create_index_html_extension(self, build_dir: str):
        for root, dirs, files in os.walk(build_dir, topdown=False):
            for name in files:
                if name == "index":
                    try:
                        os.rename(os.path.join(root, name),
                                  os.path.join(root, f"{name}.html"))
                    except Exception:
                        pass

    async def build(self):
        ROOT = os.path.dirname(os.path.abspath("./web"))

        try:
            shutil.rmtree(os.path.join(ROOT, "dist"))
        except Exception:
            pass

        await build_pages(ctx=self.context)
        await build_blog_list(ctx=self.context)
        await build_project_slug(ctx=self.context)
        await build_assets(ctx=self.context)
        await build_shared(ctx=self.context)
