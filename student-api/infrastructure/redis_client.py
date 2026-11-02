import logging
import os

import redis.asyncio as redis

logger = logging.getLogger(__name__)

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

redis_client = redis.from_url(REDIS_URL, decode_responses=True)


async def cache_get(key: str):
    """Return the cached value, or None if missing or Redis is unavailable."""
    try:
        return await redis_client.get(key)
    except redis.RedisError as exc:
        logger.warning("Redis unavailable, skipping cache read: %s", exc)
        return None


async def cache_set(key: str, value: str, ttl_seconds: int = 60):
    try:
        await redis_client.set(key, value, ex=ttl_seconds)
    except redis.RedisError as exc:
        logger.warning("Redis unavailable, skipping cache write: %s", exc)


async def cache_delete(key: str):
    try:
        await redis_client.delete(key)
    except redis.RedisError as exc:
        logger.warning("Redis unavailable, skipping cache delete: %s", exc)
