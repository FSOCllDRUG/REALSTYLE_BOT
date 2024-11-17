from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.types import FSInputFile

from create_bot import bot  # noqa
from filters.chat_type import ChatType
from filters.is_admin import IsAdmin
from keyboards.inline import admin_price
from tools.excel import json_to_excel, excel_to_json
from tools.users import send_monthly_report

admin_private_router = Router()
admin_private_router.message.filter(ChatType("private"), IsAdmin())


@admin_private_router.callback_query(F.data == "get_config")
async def get_config(callback: CallbackQuery):
    await callback.answer("")
    await json_to_excel('config.json', 'config.xlsx')
    await bot.send_document(callback.from_user.id, FSInputFile('config.xlsx'))


@admin_private_router.message(F.content_type == "document")
async def handle_docs(message: Message):
    document_id = message.document.file_id
    document = message.document
    if document.file_name == "config.xlsx":
        file_info = await bot.get_file(document_id)
        file_path = file_info.file_path
        await bot.download_file(file_path, 'config.xlsx')

        await excel_to_json('config.xlsx', 'config.json')
        await message.reply("✅Файл успешно обновлен и сохранен✅")
    else:
        await message.reply("‼️Файл должен называться↙️‼️ <pre>config.xlsx</pre>")


@admin_private_router.callback_query(F.data == "admin_menu")
async def admin_menu(callback: CallbackQuery):
    await callback.answer("")
    await callback.message.answer(text="Нажми на кнопку, чтобы выгрузить таблицу акутальных цен",
                                  reply_markup=admin_price
                                  )
    await callback.message.answer("Чтобы обновить цены в боте пришли мне изменённый файл <pre>config.xlsx</pre>\n\n"
                                  "‼️Менять только численные значения‼️\n"
                                  "‼️При десятичных числах использовать точку, а не запятую‼️")


@admin_private_router.callback_query(F.data == "users_report")
async def users_report(callback: CallbackQuery):
    await callback.answer("")
    await send_monthly_report()
