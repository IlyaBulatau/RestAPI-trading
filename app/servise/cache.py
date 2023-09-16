from aioredis import from_url, Redis

from functools import wraps
from typing import Coroutine
import json

from app.settings.config import Settings


redis: Redis = from_url(f"redis://{Settings().REDIS_HOST}", decode_responses=True, encoding="utf-8")

CACHE_PREFIX = "cache_get_requests"


def cache(ttl: int = 600):
    """
    Caches the endpoint result
    ttl - total time live(time in second) default 10min
    """
    def wrapper(func: Coroutine):

        @wraps(func)
        async def _inner(*args, **kwargs):
            #create cache key
            key = f"{CACHE_PREFIX}:{func.__name__}:{args}:{kwargs}"
            result = await redis.get(key)
            if result:
                # covert result str to dict 
                dict_result = json.loads(result)
                return dict_result

            result = await func(*args, **kwargs)
            await redis.set(key, str(result.model_dump_json()), ttl)
            return result
        return _inner
    return wrapper
            