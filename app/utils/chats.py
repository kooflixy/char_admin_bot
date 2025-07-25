
from logging import getLogger
from aiogram import Bot
from aiogram.types import Message
from aiogram.exceptions import TelegramAPIError

async def send_message_copy(bot: Bot, chat_id: int, original: Message):
    """Функция для ручного копирования сообщения со всем содержимым"""
    if original.text:
        await bot.send_message(
            chat_id=chat_id,
            text=original.text,
            entities=original.entities,
            reply_markup=original.reply_markup
        )
    elif original.photo:
        await bot.send_photo(
            chat_id=chat_id,
            photo=original.photo[-1].file_id,
            caption=original.caption,
            caption_entities=original.caption_entities,
            reply_markup=original.reply_markup
        )
    elif original.video:
        await bot.send_video(
            chat_id=chat_id,
            video=original.video.file_id,
            caption=original.caption,
            caption_entities=original.caption_entities,
            reply_markup=original.reply_markup
        )
    elif original.document:
        await bot.send_document(
            chat_id=chat_id,
            document=original.document.file_id,
            caption=original.caption,
            caption_entities=original.caption_entities,
            reply_markup=original.reply_markup
        )
    # Добавьте другие типы медиа по аналогии