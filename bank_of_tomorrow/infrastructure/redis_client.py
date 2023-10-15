import aioredis

from bank_of_tomorrow.config import get_redis_uri


class RedisClientFactory:
    def __init__(self):
        host, port = get_redis_uri()
        self.cache = aioredis.Redis(host=host, port=port)

    def get_client(self):
        return self.cache


redis_client_factory = RedisClientFactory()
