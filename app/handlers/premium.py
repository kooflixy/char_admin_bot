from logging import getLogger

from aiogram import Router
from aiogram.filters import Command, CommandObject
from aiogram.types import Message

from app.middlewares.is_admin import IsAdminFilter
from config import settings
from db import async_session_factory
from db.orm.premium_users import PremiumUsersORMHandler
from utils.telthon_manager import TelethonManager
from utils.time import utc_to_local

log = getLogger(__name__)

router = Router()


@router.message(Command("premium"), IsAdminFilter(settings.ADMIN_ID))
async def give_premium(message: Message, command: CommandObject):
    args = command.args.split()
    if len(args) != 2:
        return

    user_id, days = list(map(int, args))

    if days <= 0:
        await message.answer("Количество дней не может быть меньше нуля или равно ему")
        return

    user = await TelethonManager.get_user(user_id)

    if not user:
        await message.reply(f"Пользователя {user_id!r} не существует")
        return

    async with async_session_factory() as session:
        premium_record = await PremiumUsersORMHandler.insert(session, user_id, days)
        await session.commit()
        await session.refresh(premium_record)
        await message.reply(
            f'Пользователю {user.first_name} выдан премиум до {utc_to_local(premium_record.until_date).strftime("%Y-%m-%d %H:%M:%S")} МСК'
        )
