import os
import aioredis
from rejson import Client
from pydantic import BaseModel
from stephensanwoweb.types.cache import RedisSettings

class Redis(BaseModel):
    redis_settings: RedisSettings
    
    @property
    def redis_client(self):
        connection = aioredis.from_url(self.redis_settings.connection_url, db=0)
        return connection

    @property
    def rejson_client(self):
        return Client(host=self.redis_settings.host, port=self.redis_settings.port, decode_responses=True, username=self.redis_settings.user, password=self.redis_settings.password)



