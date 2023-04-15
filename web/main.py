import uvicorn
from web import WebMicroservice
from config import settings

service: WebMicroservice = WebMicroservice(config=settings)
api = service.create_api()

if __name__ == "__main__":
    uvicorn.run("main:api",
                host=service.settings.server.host,
                port=service.settings.server.port,
                reload=service.settings.server.reload,
                workers=service.settings.server.workers,
                ssl_keyfile=service.settings.server.ssl_keyfile,
                ssl_certfile=service.settings.server.ssl_certificate)
