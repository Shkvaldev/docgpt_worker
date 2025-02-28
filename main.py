import asyncio
import json
from aio_pika import connect_robust, Message
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
        
        buffer = {}
         
        # Hook for processing messages
        await queue.consume(
            MessageManager(buffer=buffer).handle,
            no_ack=False
        )

        if "result" in buffer:
            await channel.default_exchange.publish(
                Message(
                    body=json.dumps(buffer["answer"]).encode(),
                    ),
                    routing_key=settings.tasks_statuses_queue,
            )

        # Run forever
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())
