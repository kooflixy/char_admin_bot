import json
import os
from logging import getLogger
from typing import Optional

from dotenv import load_dotenv
from pydantic import BaseModel

log = getLogger(__name__)

load_dotenv()


def generate_CONTEXT_MESSAGES_list(context_messages: str) -> list[dict[str, str]]:
    if context_messages:
        res = []
        lst = json.loads(context_messages)

        if len(lst) % 2:
            lst = lst[: len(lst) - 1]

        for ind, content in enumerate(lst):
            if ind % 2:
                role = "assistant"
            else:
                role = "user"
            res.append(dict(role=role, content=content))
        return res
    return []


def generate_BYE_MESSAGES_list(bye_messages: str) -> list[str]:
    if bye_messages:
        return json.loads(bye_messages)
    return []


class Settings(BaseModel):
    # db
    DB_HOST: str = os.getenv("DB_HOST")
    DB_PORT: int = int(os.getenv("DB_PORT"))
    DB_USER: str = os.getenv("DB_USER")
    DB_PASS: str = os.getenv("DB_PASS")
    DB_NAME: str = os.getenv("DB_NAME")

    DATABASE_URL_asyncpg: str = (
        f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )
    DATABASE_URL_psycopg: str = (
        f"postgresql+psycopg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )

    TELETHON_API_ID: str = os.getenv("TELETHON_API_ID")
    TELETHON_API_HASH: str = os.getenv("TELETHON_API_HASH")

    TG_API_TOKEN: str = os.getenv("TG_API_TOKEN")

    ADMIN_ID: int = int(os.getenv("ADMIN_ID"))


settings = Settings()
