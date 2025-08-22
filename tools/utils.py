import json

from aiogram.types import Message


async def msg_to_cbk(message: Message):
    raw_buttons = message.text.split("\n")
    clean_buttons = {}
    for btn in raw_buttons:
        text, link = btn.split(":", maxsplit=1)
        clean_buttons[text.strip()] = link.strip()
    return clean_buttons


async def get_users_from_json():
    with open('users.json', 'r') as file:
        users_data = json.load(file)
    return list(users_data.keys())