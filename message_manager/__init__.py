from typing import Any, Dict
from aio_pika import IncomingMessage
from loguru import logger

from tasks.llm import LLM
from tasks.webwalker import WebWalker

class MessageManager:
    """
    Comes as router which choses which task to petform operations on message from rabbitmq.
    """
    def __init__(self, buffer: Dict[str, Any]) -> None:
        self.buffer = buffer
        self.links = {
            "llm": LLM,
            "webwalker": WebWalker
        }

    async def handle(self, message: IncomingMessage):
        async with message.process():
            logger.debug(f"Got message from queue: headers [ {message.headers} ], body [ {message.body.decode()} ]")
            
            type_header = message.headers.get('type') or None
            if not type_header:
                return

            for link in self.links:
                if link == type_header:
                    # Performing task and saving results to buffer
                    self.buffer["result"] = await self.links[link]().perform(message=message)
                    return
            logger.warning(f"Can not define worker for task `{message.headers.get('task_id')}`")
