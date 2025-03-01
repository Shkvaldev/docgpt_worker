from typing import Optional
from openai import AsyncOpenAI
from loguru import logger

from config import settings

class OpenAIService:
    """
    Service for dealing with OpenAI API compatible server.
    """
    def __init__(self, model: Optional[str] = None) -> None:
        """
        AI provider
        """
        if not model:
            model = settings.openai_default_model

        self.client = AsyncOpenAI( # type: ignore
            base_url=settings.openai_endpoint,
            api_key=settings.openai_api_key
        )
        self.model = model

    async def check_connection(self) -> bool:
        """
        Checks if OpenAI API server available.
        """
        try:
            await self.client.models.list()
            return True
        except Exception:
            return False

    async def ask(self, message: str, context: str = "") -> Optional[str]:
        """
        Interacts with OpenAI API server to generate answer.
        """
        try:
            result = await self.client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful AI assistant."
                    },
                    {
                        "role": "user",
                        "content": f"Using context (if provided) answer the question:\nQUESTION:{message}\nCONTEX: {context}",
                    }
                ],
                model=self.model,
            )
            return result.choices[0].message.content or None
        except Exception as e:
            logger.error(f"Error while getting answer from LLM: {e}")
