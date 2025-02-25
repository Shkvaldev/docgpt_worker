import asyncio
from aio_pika import connect_robust
from aio_pika.patterns import Master
from loguru import logger

from message_manager import MessageManager
from config import settings

async def main():
    pass

if __name__ == "__main__":
    asyncio.run(main())
