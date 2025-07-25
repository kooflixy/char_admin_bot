import json
import os
from typing import Any

SETTINGS_PATH = 'characters.json'

if not os.path.exists(SETTINGS_PATH):
    raise ImportError(f'Файл {SETTINGS_PATH} не найден')

with open(SETTINGS_PATH, 'r', encoding='utf-8') as file:
    data = json.load(file)

settings: dict[str, Any] = data['settings']
characters: list[dict[str, Any]] = data["characters"]

all_characters_settings = []

for ind, character in enumerate(characters):
    character_settings = {}
    for key, setting in settings.items():
        if key == 'exclude_keys' or key in settings["exclude_keys"]:
            continue
        
        if setting is None:
            if key not in character.keys():
                raise ValueError(f'Нет {key} в {character.get('name', ind)} персонаже')
            character_settings[key] = character[key]
        else:
            character_settings[key] = character.get(key, setting)
    
    all_characters_settings.append(character_settings)

print(all_characters_settings)