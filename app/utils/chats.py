from logging import getLogger
from aiogram import Bot
from aiogram.types import Message
from aiogram.exceptions import TelegramAPIError

log = getLogger(__name__)



async def send_message_copy(bot: Bot, chat_id: int, original: Message) -> bool:
    """Универсальная функция для копирования сообщений любого типа"""
    # 1. Текстовые сообщения
    if original.text:
        await bot.send_message(
            chat_id=chat_id,
            text=original.text,
            entities=original.entities,
            reply_markup=original.reply_markup,
            parse_mode="HTML" if original.entities else None
        )
        return True
    
    # 2. Фото
    elif original.photo:
        await bot.send_photo(
            chat_id=chat_id,
            photo=original.photo[-1].file_id,
            caption=original.caption,
            caption_entities=original.caption_entities,
            reply_markup=original.reply_markup,
            parse_mode="HTML" if original.caption_entities else None
        )
        return True
    
    # 3. Видео
    elif original.video:
        await bot.send_video(
            chat_id=chat_id,
            video=original.video.file_id,
            caption=original.caption,
            caption_entities=original.caption_entities,
            reply_markup=original.reply_markup,
            parse_mode="HTML" if original.caption_entities else None
        )
        return True
    
    # 4. Документы
    elif original.document:
        await bot.send_document(
            chat_id=chat_id,
            document=original.document.file_id,
            caption=original.caption,
            caption_entities=original.caption_entities,
            reply_markup=original.reply_markup,
            parse_mode="HTML" if original.caption_entities else None
        )
        return True
    
    # 5. Аудио
    elif original.audio:
        await bot.send_audio(
            chat_id=chat_id,
            audio=original.audio.file_id,
            caption=original.caption,
            caption_entities=original.caption_entities,
            reply_markup=original.reply_markup,
            parse_mode="HTML" if original.caption_entities else None
        )
        return True
    
    # 6. Голосовые сообщения
    elif original.voice:
        await bot.send_voice(
            chat_id=chat_id,
            voice=original.voice.file_id,
            caption=original.caption,
            reply_markup=original.reply_markup
        )
        return True
    
    # 7. Стикеры
    elif original.sticker:
        await bot.send_sticker(
            chat_id=chat_id,
            sticker=original.sticker.file_id,
            reply_markup=original.reply_markup
        )
        return True
    
    # 8. Если тип сообщения не поддерживается
    log.warning("Неподдерживаемый тип сообщения msg_type=%s", original.content_type)
    return False