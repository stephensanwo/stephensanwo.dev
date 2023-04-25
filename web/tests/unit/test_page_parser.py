"""
This file (test_spage_parse.py)
contains the unit tests for the
yml page parsers
"""
from web.utils.data_parser import (fetch_page_data)
from web.types.pages import (Page)
import os
import pytest


@pytest.mark.asyncio
async def test_blog_data_parser(blog_urls):
    """
    Test blog data parser
    """
    ROOT = os.path.dirname(os.path.abspath("./web"))

    for url in blog_urls:
        page: Page = await fetch_page_data(
            os.path.join(ROOT,
                         "web/pages/", f"{url[1]}", f"{url[0]}.yml"))

        assert page.title != ""
        assert page.meta.description != ""
        assert page.meta.title != ""
        assert page.meta.url != []
        assert page.meta.product != ""
        #  TODO Add More tests


@pytest.mark.asyncio
async def test_project_data_parser(project_urls):
    """
    Test project data parser
    """
    ROOT = os.path.dirname(os.path.abspath("./web"))

    for url in project_urls:
        page: Page = await fetch_page_data(
            os.path.join(ROOT,
                         "web/pages/projects", f"{url[0]}.yml"))

        assert page.title != ""
        assert page.meta.description != ""
        assert page.meta.title != ""
        assert page.meta.url != []
        assert page.meta.product != ""
