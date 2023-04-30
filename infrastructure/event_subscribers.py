import asyncio
import aioredis
from domain.events import ProductRegistered
from domain.models import Product
from infrastructure.repositories import MySqlProductRepository


async def process_product_registered_event(event):
    repository = MySqlProductRepository()
    product = Product(event.name, event.description, event.product_id)
    repository.add(product)


async def listen_for_events():
    redis = aioredis.from_url("redis://localhost:33001")
    async with redis.client() as conn:
        while True:
            events = await conn.xread(
                {"product_registered_stream": "$"},
                count=1,
                block=0,
            )
            for stream_events in events:
                for _, event_data in stream_events[1]:
                    print(event_data)
                    product_registered_event = ProductRegistered(
                        event_data[b"name"].decode(),
                        event_data[b"description"].decode(),
                        event_data[b"product_id"].decode(),
                    )
                    await process_product_registered_event(product_registered_event)


if __name__ == "__main__":
    asyncio.run(listen_for_events())
