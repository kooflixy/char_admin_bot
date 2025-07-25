import json
import os
from typing import Any

SETTINGS_PATH = "characters.json"
CHAR_BOT_PATH = "../charbot/"
ADMIN_BOT_PATH = "."

if not os.path.exists(SETTINGS_PATH):
    raise ImportError(f"Файл {SETTINGS_PATH} не найден")

with open(SETTINGS_PATH, "r", encoding="utf-8") as file:
    data = json.load(file)

settings: dict[str, Any] = data["settings"]
characters: list[dict[str, Any]] = data["characters"]

all_characters_settings: list[dict] = []

for ind, character in enumerate(characters):
    character_settings = {}
    for key, setting in settings.items():
        if key == "exclude_keys" or key in settings["exclude_keys"]:
            continue

        if setting is None:
            if key not in character.keys():
                raise ValueError(f"Нет {key} в {character.get('name', ind)} персонаже")
            character_settings[key] = character[key]
        else:
            character_settings[key] = character.get(key, setting)

    all_characters_settings.append(character_settings)

file_text = ""

file_text += "services:\n"

if settings["DB_HOST"] == "dbps":
    file_text += f"""
  postgres:
    image: postgres:17-alpine
    container_name: char_psgr
    restart: unless-stopped
    environment:
      - POSTGRES_USER={settings["DB_USER"]}
      - POSTGRES_PASSWORD={settings["DB_PASS"]}
      - POSTGRES_DB={settings["DB_NAME"]}
    volumes:
      - postgres-data:/var/lib/postgresql/data
    networks:
      - dbnet"""

if settings["adminer"]:
    file_text += f"""
  adminer:
    image: adminer
    container_name: char_adminer
    restart: unless-stopped
    ports:
      - "127.0.0.1:8080:8080"
    links:
      - "postgres:db"
    networks:
      - dbnet
    depends_on:
      - postgres"""

if settings["ADMIN_BOT_TG_API_TOKEN"]:
    file_text += f"""
  char_admin:
    build: {ADMIN_BOT_PATH}
    image: admin_bot
    container_name: char_admin_bot
    restart: unless-stopped
    command: sh -c "while ! nc -z postgres 5432; do sleep 1; done && alembic upgrade head && python main.py"
    environment: 
      - DB_HOST={settings["DB_HOST"]}
      - DB_PORT={settings["DB_PORT"]}
      - DB_USER={settings["DB_USER"]}
      - DB_PASS={settings["DB_PASS"]}
      - DB_NAME={settings["DB_NAME"]}
      - TG_API_TOKEN={settings["ADMIN_BOT_TG_API_TOKEN"]}
      - ADMIN_ID={settings["ADMIN_ID"]}
    links:
      - "postgres:dbps"
    networks:
      - dbnet
    volumes:
      - {CHAR_BOT_PATH}db:/app/db
    depends_on:
      - postgres"""

for character in all_characters_settings:
    env_text = ""
    for key, sett in character.items():
        if key == "name":
            continue
        if isinstance(sett, list):
            env_text += f"\n      - {key}={json.dumps(sett, ensure_ascii=False)}"
        else:
            env_text += f"\n      - {key}={sett}"

    file_text += f"""
  {character["name"]}_char:
    build: {CHAR_BOT_PATH}
    image: char_bot
    container_name: {character["name"]}_bot
    restart: unless-stopped
    command: sh -c "while ! nc -z postgres 5432; do sleep 1; done && alembic upgrade head && python main.py"
    environment: {env_text}
    links:
      - "postgres:dbps"
    networks:
      - dbnet
    depends_on:
      - char_admin"""

file_text += f"""
networks:
  dbnet:
    driver: bridge

volumes:
  postgres-data:"""

with open("compose.yml", "w", encoding="utf-8") as file:
    file.write(file_text)
