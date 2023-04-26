from web.types.pages import (Page)
from web.utils.static_site_generator import StaticSiteGenerator
from web.types.context import WebMicroserviceContext
from web.utils.data_parser import fetch_page_data, get_page_urls
from web.utils.sitemap_generator import generate_sitemap
import os


async def build_pages(ctx: WebMicroserviceContext) -> None:

    # Fetch Data from www directory
    build_config = ctx.settings.build_config

    ROOT = os.path.dirname(os.path.abspath("./web"))
    urls = get_page_urls(
        dir=build_config.domains["www"].static_dir,
        include_subdirectories=False)

    customTemplates = {
        "index": "index.html",
        "404": "404.html",
        "profile": "profile.html"
    }

    static_generator = StaticSiteGenerator(
        domain=build_config.domains["www"].domain)

    # Build pages
    for url in urls:
        output_template = "page.html"
        output_file = url[0]

        if customTemplates.get(url[0]):
            output_template = customTemplates.get(url[0])

            if url[0] == "profile":
                output_file = "profile"
            else:
                output_file = customTemplates.get(url[0])

        page: Page = await fetch_page_data(
            os.path.join(ROOT,
                         build_config.domains["www"].static_dir,
                         f"{url[1]}.yml"))

        static_generator.build(
            output_dir=os.path.join(
                ROOT, build_config.domains["www"].output_dir),
            output_file=output_file,
            output_template=output_template,
            data=page.dict(),
            create_sitemap=True
        )

    generate_sitemap(
        urls=static_generator.cache,
        output_dir=build_config.domains["www"].xml_dir)
