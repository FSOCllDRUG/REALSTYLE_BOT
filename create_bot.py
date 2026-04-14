import logging
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.enums import ParseMode
from decouple import config

from loggers.setup_logger import module_logger

env_admins = [int(admin_id) for admin_id in config("ADMINS").split(",")]
module_logger("aiogram", "logs_bot", "bot.log", logging.ERROR, console=True)

proxy_url = config("TELEGRAM_PROXY", default=None)
token = config("BOT_TOKEN")

session = AiohttpSession(proxy=proxy_url) if proxy_url else None
bot = Bot(token=token, session=session, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()
