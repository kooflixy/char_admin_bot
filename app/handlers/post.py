from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command, CommandObject

from app.middlewares.is_admin import IsAdminFilter
from app.middlewares.is_replied import IsReplyFilter
from config import settings
from db.orm.logs import LogsORMHandler

router = Router()

@router.message(Command('post'), IsReplyFilter(), IsAdminFilter(settings.ADMIN_ID))
async def post_message(message: Message, command: CommandObject):
    pass