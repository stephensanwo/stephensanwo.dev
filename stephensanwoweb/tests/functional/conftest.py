import pytest
from fastapi.testclient import TestClient
from stephensanwoweb import WebMicroservice

service: WebMicroservice = WebMicroservice()
api = service.create_api()

@pytest.fixture(scope="module")
def client():
    return TestClient(api)

@pytest.fixture(scope="module")
def context():
    return service.context