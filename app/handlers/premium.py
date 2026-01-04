from datetime import datetime
from logging import getLogger

from aiogram import Bot, Router
from aiogram.filters import Command, CommandObject
from aiogram.types import Message

from app.middlewares.is_admin import IsAdminFilter
from app.utils.data_manager import JSONManager
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

    async with async_session_factory() as session:
        premium_record = await PremiumUsersORMHandler.insert(session, user_id, days)
        await session.commit()
        await session.refresh(premium_record)
        await message.reply(
            f'Пользователю {user_id} выдан премиум до {utc_to_local(premium_record.until_date).strftime("%Y-%m-%d %H:%M")} МСК'
        )

    characters = JSONManager.get_json("characters.json")["characters"]
    for char in characters:
        async with Bot(token=char["TG_API_TOKEN"]) as bot:
            try:
                await bot.send_message(
                    user_id,
                    f'🎉Поздравляем, Вы активировали премиум до {utc_to_local(premium_record.until_date).strftime("%Y-%m-%d %H:%M")} МСК',
                )
                await bot.close()
            except:
                pass
    log.info("Был дан премиум premium_user_id=%s", user_id)


@router.message(Command("premium_list"), IsAdminFilter(settings.ADMIN_ID))
async def get_premium_list(message: Message, command: CommandObject):
    async with async_session_factory() as session:
        premium_records_list = await PremiumUsersORMHandler.get_all_current(session)

    text_list = [
        f"Количество: {len(premium_records_list)}\n",
        "💳Список премиум пользователей:\n",
    ]

    for ind, premium_record in enumerate(premium_records_list):
        local_until_date = utc_to_local(premium_record.until_date)

        user = await TelethonManager.get_user(premium_record.user_id)

        str_ = f"🌟Пользователь: <code>{user.first_name}</code>\n"
        str_ += f"\tID: <code>{premium_record.user_id}</code>\n"
        str_ += f'\tДо: {local_until_date.strftime("%Y-%m-%d %H:%M")} МСК\n'
        text_list.append(str_)

        if not ind % 20 and ind:
            str_ = "\n".join(text_list)
            await message.reply(str_)
            text_list = []

    if not len(premium_records_list) or not ind or ind % 20:
        str_ = "\n".join(text_list)
        await message.reply(str_)
