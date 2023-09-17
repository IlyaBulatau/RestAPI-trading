from aioredis import from_url, Redis

from functools import wraps
from typing import Coroutine
import json

from app.settings.constance import CACHE_TTL_SEC
from app.settings.config import Settings


redis: Redis = from_url(
    f"redis://{Settings().REDIS_HOST}", decode_responses=True, encoding="utf-8"
)

CACHE_PREFIX = "cache_get_requests"


def cache(ttl: int = CACHE_TTL_SEC):
    """
    Caches the endpoint result
    ttl - total time live(time in second) default 10min
    """

    def wrapper(func: Coroutine):
        @wraps(func)
        async def _inner(*args, **kwargs):
            # create cache key
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


def cache_reset(func_name):
    """
    Search all cache result in redis
    using pattern consisting of
    variable - CACHE_PREFIC, accept argument - func_name and then any symbols

    Used in POST requests to provide fresh data in GET requests
    """

    def wrapper(func: Coroutine):
        @wraps(func)
        async def _inner(*args, **kwargs):
            # create a search pattern
            key = f"{CACHE_PREFIX}:{func_name}:*"
            # search by pattern
            async for k in redis.scan_iter(match=key):
                # delete all result
                await redis.delete(k)

            return await func(*args, **kwargs)

        return _inner

    return wrapper
