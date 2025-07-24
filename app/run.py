from aiogram import Dispatcher

from app.handlers import *
from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums.parse_mode import ParseMode

from config import settings

bot = Bot(
    token=settings.TG_API_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML),
)


async def run():
    dp = Dispatcher()

    # fmt: off
    dp.include_routers(
    )
    # fmt: on

    await bot.delete_webhook(drop_pending_updates=True)
    print("start")
    await dp.start_polling(bot)
