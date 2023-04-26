from web.utils.static_site_generator import StaticSiteGenerator
from web.types.context import WebMicroserviceContext
from web.utils.data_parser import fetch_page_data, get_page_urls
from web.utils.sitemap_generator import generate_sitemap
from web.types.pages import (Page)
import os


async def build_project_slug(ctx: WebMicroserviceContext):
    # Fetch Data from project directory
    build_config = ctx.settings.build_config
    ROOT = os.path.dirname(os.path.abspath("./web"))

    urls = get_page_urls(
        dir=build_config.domains["projects"].static_dir,
        include_subdirectories=False)

    customTemplates = {
        "index": "index.html",
        "404": "404.html",
    }

    # Initialize Static Site Generator
    static_generator = StaticSiteGenerator(
        domain=build_config.domains["projects"].domain)

    for url in urls:
        output_file = url[0]
        if customTemplates.get(url[0]):
            output_file = customTemplates.get(url[0])

        page: Page = await fetch_page_data(
            os.path.join(
                ROOT,
                build_config.domains["projects"].static_dir,
                f"{url[0]}.yml"))

        # Generate static HTML for Projects List Slugs
        static_generator.build(
            output_dir=os.path.join(
                ROOT,
                build_config.domains["projects"].output_dir),
            output_file=output_file,
            output_template="page.html",
            data=page.dict(),
            create_sitemap=True
        )

    generate_sitemap(
        urls=static_generator.cache,
        output_dir=build_config.domains["projects"].xml_dir)
