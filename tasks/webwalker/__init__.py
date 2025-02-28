from typing import Dict, Optional, Any
from aio_pika import IncomingMessage
from loguru import logger

class WebWalker:
    """
    Agent that uses playwright to serve the Web
    """
    async def perform(self, message: IncomingMessage) -> Optional[Dict[str, Any]]:
        logger.debug(f"Processing WebWalker task `{message.headers.get('task_id')}`")
        return {'message': message.body.decode()}
