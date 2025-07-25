from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums.parse_mode import ParseMode

from app.handlers import *
from config import settings

bot = Bot(
    token=settings.TG_API_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML),
)


async def run():
    dp = Dispatcher()

    # fmt: off
    dp.include_routers(
        post.router,
        stats.router
    )
    # fmt: on

    await bot.delete_webhook(drop_pending_updates=True)
    print("start")
    await dp.start_polling(bot)
