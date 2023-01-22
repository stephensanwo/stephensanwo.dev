from stephensanwoweb.types.routes import (Routes, BackendRoutes, ProjectRoutes)
import pytest

def test_routes(client):
    for route in Routes:
        response = client.get(f"/{route.value}")
        assert response.status_code == 200

def test_backend_routes(client):
    for route in [BackendRoutes.admin.value, BackendRoutes.dashboard.value, BackendRoutes.blog.value]:
        response = client.get(f"{route}")
        assert response.status_code == 200

def test_project_routes(client):
    for route in ProjectRoutes:
        response = client.get(f"{route.value}")
        assert response.status_code == 200

@pytest.mark.asyncio
async def test_blog_routes(client, context):
    blog_list = await context.cache.get_json(key="blog_data")
    print(blog_list)
    pass
