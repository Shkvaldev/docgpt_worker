from typing import Dict, Optional, Any
from aio_pika import IncomingMessage
from loguru import logger

class LLM:
    """
    Agent that uses AI to answer questions
    """
    async def perform(self, message: IncomingMessage) -> Optional[Dict[str, Any]]:
        logger.debug(f"Processing AiChat task `{message.headers.get('task_id')}`")
        return {'message': message.body.decode()}
