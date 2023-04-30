import aioredis
from domain.events import ProductRegistered


class RedisEventPublisher:
    async def publish(self, event):
        redis = aioredis.from_url("redis://localhost:33001")
        async with redis.client() as conn:
            if isinstance(event, ProductRegistered):
                await conn.xadd(
                    "product_registered_stream",
                    {
                        "name": event.name,
                        "description": event.description,
                    },
                )
