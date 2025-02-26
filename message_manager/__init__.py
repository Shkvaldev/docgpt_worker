from aio_pika import IncomingMessage
from loguru import logger

class MessageManager:
    """
    Comes as router which choses which task to petform operations on message from rabbitmq.
    """
    async def handle(self, message: IncomingMessage):
        async with message.process():
            logger.debug(f"Got message from queue: {message.body.decode()}")
