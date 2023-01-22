import json
from . import Redis
from datetime import timedelta
from rejson import Path
from typing import Optional

class RedisInterface(Redis):

    async def store_cache_data(self, cache_timeout:int, key: str, value: dict | list) -> bool:
        return await self.redis_client.set(key, json.dumps(value), ex=timedelta(seconds=cache_timeout))
    
    async def get_cache_data(self, key: str) -> dict | list:
        data = await self.redis_client.get(key)
        if data != None:
            return json.loads(data)
        else:
            return data        

    async def get_json(self, key: str, path: Optional[str] = ""):
        if path:
            return self.rejson_client.jsonget(
            key, Path(path))
        
        else:
            return self.rejson_client.jsonget(
            key, Path.rootPath())

    async def store_json(self, key: str, data: dict, path: Optional[str]):
        key_exists = self.rejson_client.jsonget(
            key, Path.rootPath())
        if key_exists==None:
            self.rejson_client.jsonset(key, Path.rootPath(), {})
            
        self.rejson_client.jsonset(key, Path(path), data)

    async def delete_json(self, key: str, path: str):
        self.rejson_client.jsondel(key, Path(path))