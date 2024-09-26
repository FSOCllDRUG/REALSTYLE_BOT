import asyncio
from functools import partial

from aiogram.types import BotCommand, BotCommandScopeDefault

from create_bot import bot, dp, env_admins
from handlers.admin_private import admin_private_router
from handlers.user_router import user_router


async def set_commands():
    commands = [BotCommand(command="start", description="Перезапуск бота")]
    await bot.set_my_commands(commands, BotCommandScopeDefault())


async def start_bot():
    await set_commands()
    try:
        for admin_id in env_admins:
            await bot.send_message(admin_id, f"Бот запущен🥳")
    except:
        pass


async def stop_bot():
    try:
        for admin_id in env_admins:
            await bot.send_message(admin_id, "Бот остановлен.\n😴")
    except:
        pass


async def main():
    dp.include_router(user_router)
    dp.include_router(admin_private_router)

    dp.startup.register(partial(start_bot))  # Передаем сессию в start_bot
    dp.shutdown.register(stop_bot)

    try:
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
