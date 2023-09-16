from aioredis import from_url, Redis


from app.settings.config import Settings


redis: Redis = from_url(f"redis://{Settings().REDIS_HOST}")
