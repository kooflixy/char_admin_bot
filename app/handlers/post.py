from logging import getLogger
from aiogram import Bot, Router
from aiogram.filters import Command, CommandObject
from aiogram.types import Message
from app.utils.chats import send_message_copy
from db.orm.logs import LogsORMHandler

from app.middlewares.is_admin import IsAdminFilter
from app.middlewares.is_replied import IsReplyFilter
from app.utils.data_manager import JSONManager
from config import settings

from aiogram import Bot, Router
from aiogram.types import Message
from aiogram.exceptions import TelegramAPIError
import logging
from typing import Optional

router = Router()
logger = logging.getLogger(__name__)


@router.message(Command("post"), IsReplyFilter(), IsAdminFilter(settings.ADMIN_ID))
async def post_message(message: Message, command: CommandObject):
    original = message.reply_to_message
    
    characters = JSONManager.get_json("characters.json")["characters"]
    success_count = 0
    fail_count = 0
    
    for char in characters:
        bot = Bot(token=char["TG_API_TOKEN"])
        chat_ids = await LogsORMHandler.get_post_chats(bot.id)
        for chat_id in chat_ids:
            try:
                if await send_message_copy(bot, chat_id, original):
                    success_count += 1
                else:
                    fail_count += 1
            except:
                fail_count +=1
    
    await message.answer(
        f"📊 Результат рассылки:\n"
        f"✅ Успешно: {success_count}\n"
        f"❌ Ошибок: {fail_count}"
    )