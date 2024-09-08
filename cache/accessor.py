import redis
from sqlalchemy import select

from settings import settings

def get_redis_connection() -> redis.Redis:
    return redis.Redis(
        host=settings.CACHE_HOST,
        port=settings.CACHE_PORT,
        db=settings.CACHE_DB
    )


