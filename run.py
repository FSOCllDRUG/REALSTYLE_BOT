import asyncio
from functools import partial

from aiogram.types import BotCommand, BotCommandScopeDefault
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from create_bot import bot, dp, env_admins
from handlers.admin_private import admin_private_router
from handlers.user_router import user_router
from tools.users import send_previous_month_report, send_monthly_report  # noqa


async def set_commands():
    commands = [BotCommand(command="start", description="Restart the bot"),
                BotCommand(command="dev", description="Developer contact")]
    await bot.set_my_commands(commands, BotCommandScopeDefault())


async def start_bot():
    try:
        await set_commands()
        for admin_id in env_admins:
            await bot.send_message(admin_id, "Бот запущен🥳")
    except Exception as e:
        print(f"start_bot error: {e}")


async def stop_bot():
    try:
        for admin_id in env_admins:
            await bot.send_message(admin_id, "Бот остановлен😴")
    except:
        pass


def main():
    dp.include_router(user_router)
    dp.include_router(admin_private_router)

    dp.startup.register(partial(start_bot))
    dp.shutdown.register(stop_bot)

    scheduler = AsyncIOScheduler()
    scheduler.add_job(send_previous_month_report, 'cron', day=1, hour=0, minute=0)
    scheduler.start()

    dp.run_polling(bot, skip_updates=True)  # skip_updates заменяет delete_webhook


if __name__ == "__main__":
    main()
