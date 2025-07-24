import asyncio

from app import run as tg_bot
from config.logging_config import logging_configure


async def main():
    await tg_bot.run()


if __name__ == "__main__":
    logging_configure(filemode="w")

    asyncio.run(main())
