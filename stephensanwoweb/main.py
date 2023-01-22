import uvicorn
import multiprocessing
from stephensanwoweb.types.server import Server
from stephensanwoweb.types.metadata import Environment
from stephensanwoweb import WebMicroservice



def number_of_workers():
    print((multiprocessing.cpu_count() * 2) + 1)
    return (multiprocessing.cpu_count() * 2) + 1


service: WebMicroservice = WebMicroservice()
print(service.settings)

api = service.create_api()

if __name__ == "__main__":
    if service.settings.metadata.environment == Environment.dev :
        server: Server = service.settings.server[Environment.dev]
        uvicorn.run("main:api", host=server.host,
                    port=server.port, reload=server.reload, workers=server.workers, ssl_keyfile=server.ssl_keyfile, ssl_certfile=server.ssl_certificate)


