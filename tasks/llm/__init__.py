import json
from typing import Dict, Optional, Any
from aio_pika import IncomingMessage
from loguru import logger

from schemas import TaskStatus
from services.openai import OpenAIService

class LLM:
    """
    Agent that uses AI to answer questions
    """
    async def perform(self, message: IncomingMessage) -> Optional[TaskStatus]:
        task_id = message.headers.get('task_id') 
        logger.debug(f"Processing AiChat task `{task_id}`")
        
        # Getting task data
        task_data = json.loads(message.body.decode())

        # TODO!: add getting categories via API + make it in cycle
        context = ""

        # Generating LLM response
        answer = await OpenAIService().ask(message=task_data["message"], context=context)

        result = TaskStatus(
            task_id=task_id,
            status="done",
            data={
                'processor':'llm',
                'content': answer,
                'chat_id': task_data['chat_id'],
                'user_id': task_data['user_id']
            }
        )
        return result
