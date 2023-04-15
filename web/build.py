import asyncio
from web.build import StaticBuild


if __name__ == "__main__":
    static_build = StaticBuild()
    asyncio.run(static_build.build())
