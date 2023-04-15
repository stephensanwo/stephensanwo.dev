from web.utils.static_site_generator import StaticSiteGenerator
from web.types.context import WebMicroserviceContext
import os


async def build_assets(ctx: WebMicroserviceContext) -> None:
    # Empty string is index page
    build_config = ctx.settings.build_config
    assets: list[str] = ["js", "assets", "css", "root"]

    ROOT = os.path.dirname(os.path.abspath("./web"))

    static_generator = StaticSiteGenerator()

    for _, domain in build_config.domains.items():
        # shared domain is for public assets and does not need static files
        if domain.name != "shared":
            for asset in assets:
                if asset != "root":
                    static_generator.transfer_assets(
                        source_path=os.path.join(ROOT, "static", f"{asset}"),
                        output_dir=os.path.join(ROOT, "dist/static",
                                                f"{asset}"))

                else:
                    for file in os.listdir(os.path.join(ROOT, "static")):
                        if os.path.isfile(os.path.join(ROOT, "static",
                                                       f"{file}")):
                            static_generator.transfer_assets(
                                source_path=os.path.join(ROOT,
                                                         "static",
                                                         f"{file}"),
                                output_dir=os.path.join(ROOT,
                                                        "dist/static",
                                                        f"{file}"))
