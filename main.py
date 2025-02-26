import asyncio
from aio_pika import connect_robust
from aio_pika.patterns import Master
from loguru import logger

from message_manager import MessageManager
from config import settings

# Entrypoint
async def main():
    connection = await connect_robust(
        settings.get_rabbitmq_uri()
    )
    async with connection:
        channel = await connection.channel()
        queue = await channel.declare_queue(
            settings.tasks_queue
        )

        # Hook for processing messages
        await queue.consume(
            MessageManager().handle,
            no_ack=False
        )

        # Run forever
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())
