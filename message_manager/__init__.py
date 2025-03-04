from typing import Optional 
import json
import asyncio
from aio_pika import IncomingMessage, Message
from loguru import logger

from schemas import TaskStatus
from tasks import LLM, WebWalker
from config import settings

class MessageManager:
    """
    Comes as router which choses which task to perform operations on message from rabbitmq.
    """
    def __init__(self, channel) -> None:
        self.channel = channel
        self.links = {
            "llm": LLM,
            "webwalker": WebWalker
        }

    async def publish_answer(self, payload: TaskStatus):
        """
        Publishes answer to rabbitmq.
        """
        # Declarating result queue for sure
        await self.channel.declare_queue(
            settings.tasks_statuses_queue
        )
        # Publishing
        try:
            await self.channel.default_exchange.publish(
                Message(
                    body=json.dumps(payload.model_dump()).encode(),
                    headers={"task_id": payload.task_id}
                    ),
                    routing_key=settings.tasks_statuses_queue,
            )
        except Exception as e:
            err_msg = f"Failed to publish answer to queue: {e}"
            logger.error(err_msg)
            raise ValueError(err_msg)

    async def handle(self, message: IncomingMessage):
        async with message.process():
            logger.debug(f"Got message from queue: headers [ {message.headers} ], body [ {message.body.decode()} ]")
            
            type_header = message.headers.get('type') or None
            if not type_header:
                return

            for link in self.links:
                if link == type_header:
                    # Performing task and publishing answer to the result queue
                    task = asyncio.create_task(
                        self.links[link]().perform(message=message)
                    )
                    
                    payload: TaskStatus = await task
                    
                    # If no answer from worker - ignore
                    if not payload:
                        return

                    try:
                        await self.publish_answer(payload=payload)
                    except Exception as e:
                        logger.error(f"Failed to handle message from rabbitmq: {e}")
                    return
            logger.warning(f"Can not define worker for task `{message.headers.get('task_id')}`")
