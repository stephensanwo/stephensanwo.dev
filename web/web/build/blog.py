import os
from web.types.pages import (Cards, Page)
from web.utils.static_site_generator import StaticSiteGenerator
from web.types.context import WebMicroserviceContext
from web.utils.data_parser import fetch_page_data, get_page_urls
from web.utils.sitemap_generator import generate_sitemap
from web.utils.rss_generator import RSS
import math


async def build_blog_list(ctx: WebMicroserviceContext):
    # Fetch Data from blog directory
    build_config = ctx.settings.build_config

    ROOT = os.path.dirname(os.path.abspath("./web"))
    urls = get_page_urls(
        dir=build_config.domains["blog"].static_dir,
        include_subdirectories=True)

    cards: list[Cards] = []

    # Get new rss parser
    rss = RSS()

    # Get new static site generator
    static_generator = StaticSiteGenerator(
        domain=build_config.domains["blog"].domain)

    for url in urls:
        #  Do not include index and 404 in blog list
        if url[0] not in ["index", "404"]:
            page: Page = await fetch_page_data(
                os.path.join(ROOT,
                             "web", "pages", f"{url[1]}", f"{url[0]}.yml"))

            read_time = 1
            try:
                read_time = math.ceil(
                    len(page.data.body[0].content) / (250 * 4.7))
            except IndexError:
                pass

            cards.append(
                Cards(
                    id=f"{url[1]}/{url[0]}",
                    title=page.title,
                    description=page.data.caption,
                    url=f"{url[1]}/{url[0]}",
                    dateUpdated=page.last_update.split(" ")[0],
                    coverImage=page.meta.image,
                    readTime=read_time,
                    isInfographic=True if page.meta.product == "Infographics"
                    else False,
                    category=f"{page.data.tags[0]}",
                    author=page.meta.authors[0]
                ).dict()
            )

            # Generate static HTML for Blog List Slugs
            static_generator.build(
                output_dir=os.path.join(ROOT, "dist", f"{url[1]}"),
                output_file=f"{url[0]}",
                output_template="page.html",
                data=page.dict(),
                create_sitemap=True
            )

            # Generate rss feed for blog slug
            rss.generate_rss(
                title=page.title,
                link=f"https://blog.stephensanwo.dev/{url[0]}",
                description=page.data.caption)

        elif url[0] == "404":
            page: Page = await fetch_page_data(
                os.path.join(ROOT, "web/pages/blog/404.yml"))

            static_generator.build(
                output_dir=os.path.join(
                    ROOT,
                    build_config.domains["blog"].output_dir),
                output_file=f"{url[0]}.html",
                output_template="404.html",
                data=page.dict(),
                create_sitemap=True
            )

    # Save rss feed
    await rss.build_rss(
        output_dir=os.path.join(
            ROOT,
            build_config.domains["blog"].output_dir))

    # Build blog list page
    blog_list_page: Page = await fetch_page_data(
        os.path.join(ROOT, "web/pages/blog/index.yml"))

    blog_list_page.data.cards = list(reversed(cards))

    #  Generate static HTML for Blog List Page
    static_generator.build(
        output_dir=os.path.join(
            ROOT, build_config.domains["blog"].output_dir),
        output_file="index.html",
        output_template="page.html",
        data=blog_list_page.dict(),
        create_sitemap=True
    )

    generate_sitemap(
        urls=static_generator.cache,
        output_dir=build_config.domains["blog"].output_dir)
