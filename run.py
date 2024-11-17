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
    await set_commands()
    try:
        for admin_id in env_admins:
            await bot.send_message(admin_id, "Бот запущен🥳")
    except:
        pass


async def stop_bot():
    try:
        for admin_id in env_admins:
            await bot.send_message(admin_id, "Бот остановлен😴")
    except:
        pass


async def main():
    dp.include_router(user_router)
    dp.include_router(admin_private_router)

    dp.startup.register(partial(start_bot))  # Passing the session to start_bot
    dp.shutdown.register(stop_bot)

    # Scheduler initialization
    scheduler = AsyncIOScheduler()
    # Adding a job to the scheduler to call the handler every month
    scheduler.add_job(send_previous_month_report, 'cron', day=1, hour=0,
                      minute=0)  # Run at 00:00 on the first day of each month
    # For testing every minute:
    # scheduler.add_job(send_monthly_report, 'interval', minutes=1)
    # Starting the scheduler
    scheduler.start()

    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
