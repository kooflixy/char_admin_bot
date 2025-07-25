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

router = Router()

log = getLogger(__name__)

@router.message(Command("post"), IsReplyFilter(), IsAdminFilter(settings.ADMIN_ID))
async def post_message(message: Message, command: CommandObject):
    characters = JSONManager.get_json("characters.json")["characters"]
    
    for char in characters:
        bot = Bot(char["TG_API_TOKEN"])
        for chat_id in await LogsORMHandler.get_post_chats(bot.id):
            try:
                await send_message_copy(bot, chat_id, message.reply_to_message)
            except:
                log.exception('При отправлении поста произошла ошибка chat_id=%s bot_id=%s', chat_id, bot.id)
