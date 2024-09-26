import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from decouple import config

from loggers.setup_logger import module_logger

env_admins = [int(admin_id) for admin_id in config("ADMINS").split(",")]

module_logger("aiogram", "logs_bot", "bot.log", logging.INFO, console=True)
bot = Bot(token=config("BOT_TOKEN"), default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()
