from redis import Redis
import redis.asyncio as aioredis

from settings import REDIS_URL

async def init_redis_pool() -> aioredis.Redis:
    redis_client = await aioredis.from_url(
        REDIS_URL,
        encoding = "utf-8",
        decode_responses = True
    )

    return redis_client