import json
from datetime import datetime, timedelta

import aiofiles
from decouple import config

from create_bot import bot


# Функция для загрузки данных пользователей из файла
async def load_users():
    try:
        async with aiofiles.open("users.json", "r", encoding="utf-8") as f:
            return json.loads(await f.read())
    except FileNotFoundError:
        return {}


# Функция для сохранения данных пользователей в файл
async def save_users(users):
    async with aiofiles.open("users.json", "w", encoding="utf-8") as f:
        await f.write(json.dumps(users, ensure_ascii=False, indent=4))


# Функция для добавления нового пользователя
async def add_user(user_id):
    users = await load_users()
    if user_id not in users:
        users[user_id] = {
            "date_added": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        await save_users(users)


# Функция для подсчета общего количества пользователей
async def count_total_users():
    users = await load_users()
    return len(users)


# Функция для подсчета новых пользователей за текущий месяц
async def count_new_users():
    users = await load_users()
    previous_month = (datetime.now() - timedelta(days=30)).month
    new_users = [user for user in users.values() if
                 datetime.strptime(user["date_added"], "%Y-%m-%d %H:%M:%S").month == previous_month]
    return len(new_users)


async def count_new_users_this_month():
    users = await load_users()
    current_month = datetime.now().month
    new_users = [user for
                 user in users.values() if
                 datetime.strptime(user["date_added"], '%Y-%m-%d %H:%M:%S').month == current_month]
    return len(new_users)


async def send_monthly_report():
    print("send_monthly_report")
    total_users_count = await count_total_users()
    new_users_count = await count_new_users_this_month()
    report_message = (f"Отчет за текущий месяц:\n"
                      f"Новых пользователей: {new_users_count}\n"
                      f"Общее количество пользователей: {total_users_count}")
    for admin in config("ADMINS").split(", "):
        await bot.send_message(admin, report_message)


# Функция для отправки отчета в конце месяца
async def send_previous_month_report():
    print("send_previous_month_report")
    total_users_count = await count_total_users()
    new_users_count = await count_new_users()
    report_message = (
        f"Отчет за предыдущий месяц:\n"
        f"Общее количество пользователей: {total_users_count}\n"
        f"Количество новых пользователей: {new_users_count}")
    for admin in config("ADMINS").split(", "):
        await bot.send_message(admin, report_message)
