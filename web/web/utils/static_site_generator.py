from jinja2 import Environment, FileSystemLoader, Template
from pydantic import BaseModel
import os
from pathlib import Path
from typing import Optional
import shutil


class StaticSiteGenerator(BaseModel):
    domain: Optional[str]
    cache: list[str] = []

    def __init__(self, **data) -> list[str]:
        super().__init__(**data)
        self.cache.append(self.domain)

    def prod_url_for(self, *args, **kwargs):
        # Will update the url_for method in jinja2
        # which calls the static mount in local development
        return self.domain + kwargs["path"]

    def build(self,
              output_dir: str,
              output_file: str,
              output_template: str,
              data: dict,
              create_sitemap: bool,
              ) -> None:

        ROOT = os.path.dirname(os.path.abspath("./web"))
        source_path = os.path.join(ROOT, "static/html")
        template_env: Environment = Environment(loader=FileSystemLoader(
            searchpath=source_path))
        template: Template = template_env.get_template(output_template)
        print(f"Building static pages for -> {output_file}")

        if create_sitemap:
            # Exclude 404 and index from sitemap
            if output_file != "404.html" and output_file != "index.html":
                self.cache.append(f"{self.domain}/{output_file}")

        template.environment.globals["url_for"] = self.prod_url_for

        if not os.path.isdir(output_dir):
            try:
                Path(output_dir).mkdir(parents=True, exist_ok=True)
            except OSError as e:
                print(f"Error creating build directory -> {e}")

        with open(os.path.join(output_dir, output_file), 'w+') as f:
            f.write(template.render(data))

    def transfer_assets(self, source_path: str, output_dir: str) -> None:
        print("Transferring static assets")

        try:
            shutil.copytree(source_path, output_dir)
        except NotADirectoryError:
            shutil.copyfile(source_path, output_dir)
        except FileExistsError:
            shutil.rmtree(output_dir)
            shutil.copytree(source_path, output_dir)
