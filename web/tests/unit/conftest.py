import pytest
from web.utils.data_parser import (get_page_urls)


@pytest.fixture(scope="module")
def blog_urls():
    return get_page_urls(dir="web/pages/blog",
                         include_subdirectories=True)


@pytest.fixture(scope="module")
def project_urls():
    return get_page_urls(dir="web/pages/projects",
                         include_subdirectories=False)
