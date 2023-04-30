from domain.events import ProductRegistered
from infrastructure.event_publishers import RedisEventPublisher


class RegisterProductCommand:
    def __init__(self, name, description):
        self.name = name
        self.description = description

    async def execute(self):
        event = ProductRegistered(
            name=self.name,
            description=self.description,
        )
        publisher = RedisEventPublisher()
        await publisher.publish(event)
