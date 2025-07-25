from logging import getLogger

from aiogram import Router
from aiogram.filters import Command, CommandObject
from aiogram.types import Message
from db import async_session_factory
from db.orm.logs import LogsORMHandler

from app.middlewares.is_admin import IsAdminFilter
from config import settings

log = getLogger(__name__)

router = Router()


@router.message(Command("stats"), IsAdminFilter(settings.ADMIN_ID))
async def get_stats(message: Message, command: Command):
    async with async_session_factory() as session:
        unique_users = await LogsORMHandler.get_unique_user_count(session)
        group_count = await LogsORMHandler.get_group_count(session)
        request_count = await LogsORMHandler.get_requests_count(session)

        await message.reply(
            f"Пользователей: {unique_users}\n"
            f"Групп: {group_count}\n"
            f"Запросов: {request_count}"
        )
