from typing import Dict, Optional, Any
from aio_pika import IncomingMessage
from loguru import logger

from schemas import TaskStatus

class WebWalker:
    """
    Agent that uses playwright to serve the Web
    """
    async def perform(self, message: IncomingMessage) -> Optional[TaskStatus]:
        task_id = message.headers.get('task_id')
        logger.debug(f"Processing WebWalker task `{task_id}`")
        result = TaskStatus(
            task_id=task_id,
            status="done",
            data={'processor':'webwalker', 'message': message.body.decode()}
        )
        return result
