from web.utils.static_site_generator import StaticSiteGenerator
from web.types.context import WebMicroserviceContext
import os


async def build_shared(ctx: WebMicroserviceContext) -> None:
    # Empty string is index page
    build_config = ctx.settings.build_config

    ROOT = os.path.dirname(os.path.abspath("./web"))

    static_generator = StaticSiteGenerator(
        domain=build_config.domains["shared"].domain
    )

    static_generator.transfer_assets(
        source_path=os.path.join(
            ROOT, build_config.domains["shared"].static_dir),
        output_dir=os.path.join(ROOT,
                                build_config.domains["shared"].output_dir))
