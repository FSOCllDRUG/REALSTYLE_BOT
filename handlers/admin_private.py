# -*- coding: utf-8 -*-
from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove
from aiogram.types import FSInputFile
from aiogram.utils.chat_action import ChatActionSender

from create_bot import bot  # noqa
from filters.chat_type import ChatType
from filters.is_admin import IsAdmin
from keyboards.inline import admin_price, get_callback_btns
from keyboards.reply import get_keyboard
from tools.excel import json_to_excel, excel_to_json
from tools.mailing import simple_mailing
from tools.texts import cbk_msg
from tools.users import send_monthly_report
from tools.utils import msg_to_cbk, get_users_from_json

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


class Mailing(StatesGroup):
    message = State()
    buttons = State()


# Mailing handlers starts
@admin_private_router.callback_query(StateFilter(None), F.data == "create_mailing")
async def make_mailing(callback: CallbackQuery, state: FSMContext):
    await callback.answer("")
    await callback.message.answer("Отправь сообщение, которое ты хочешь рассылать\n\n"
                                  "<b>ВАЖНО</b>\n\n"
                                  "В рассылке может быть приложен только <u>один</u> файл*!\n"
                                  "<i>Файл— фото/видео/документ/голосовое сообщение/видео сообщение</i>",
                                  reply_markup=get_keyboard("Отмена",
                                                            placeholder="Отправьте сообщение, для рассылки"
                                                            )
                                  )
    await state.set_state(Mailing.message)


@admin_private_router.message(StateFilter(Mailing.message))
async def get_message_for_mailing(message: Message, state: FSMContext):
    await state.update_data(message=message.message_id)
    await state.set_state(Mailing.buttons)
    await message.reply("Будем добавлять URL-кнопки к сообщению?", reply_markup=await get_callback_btns(
        btns={"Добавить кнопки": "add_btns",
              "Приступить к рассылке": "confirm_mailing", "Сделать другое сообщение для рассылки": "cancel_mailing"}
    )
                        )


@admin_private_router.callback_query(StateFilter(Mailing.buttons), F.data == "add_btns")
async def add_btns_mailing(callback: CallbackQuery):
    await callback.answer("")
    await callback.message.answer(cbk_msg)


@admin_private_router.message(StateFilter(Mailing.buttons), F.text.contains(":"))
async def btns_to_data(message: Message, state: FSMContext):
    await state.update_data(buttons=await msg_to_cbk(message))
    data = await state.get_data()
    await message.answer(f"Вот как будет выглядеть сообщение в рассылке:"
                         f"\n⬇️")
    await bot.copy_message(chat_id=message.from_user.id, from_chat_id=message.chat.id, message_id=data[
        "message"],
                           reply_markup=await get_callback_btns(btns=data["buttons"]))
    await message.answer("Приступим к рассылке?",
                         reply_markup=await get_callback_btns(btns={"Да": "confirm_mailing",
                                                                    "Переделать": "cancel_mailing"}))


@admin_private_router.callback_query(StateFilter(Mailing.message), F.data == "cancel_mailing")
@admin_private_router.callback_query(StateFilter(Mailing.buttons), F.data == "cancel_mailing")
async def cancel_mailing(callback: CallbackQuery, state: FSMContext):
    await callback.answer("")
    current_state = await state.get_state()

    if current_state is not None:
        await state.set_state(Mailing.message)
        await callback.message.answer("Отправь сообщение, которое ты хочешь рассылать")


@admin_private_router.callback_query(StateFilter("*"), F.data == "confirm_mailing")
async def confirm_mailing(callback: CallbackQuery, state: FSMContext):
    async with ChatActionSender.typing(bot=bot, chat_id=callback.message.from_user.id):
        await callback.answer("")

        # Получаем данные из состояния
        data = await state.get_data()

        # Получаем список пользователей из users.json
        users = await get_users_from_json()

        # Создаем словарь с данными для рассылки
        mailing_data = {
            "users": users,
            "message_id": data.get("message"),
            "chat_id": str(callback.message.chat.id),
            "buttons": data.get("buttons")
        }
        
        await state.clear()

        success, notsuccess, blocked, elapsed_time_str = await simple_mailing(mailing_data)
        if elapsed_time_str == "":
            elapsed_time_str = "менее секунды"

        await callback.message.answer(
            text=f"Рассылка успешна.\n\nРезультаты:\nУспешно - {success}\nНеудачно - {notsuccess}\n\n"
                 f"Затрачено времени: <b>{elapsed_time_str}</b>\n\n"
                 f"<span class='tg-spoiler'>Бот заблокирован у {blocked} пользователя(ей)</span>",
            reply_markup=ReplyKeyboardRemove()
        )
        await callback.message.answer("Вернемся в меню?",
                                      reply_markup=await get_callback_btns(btns={"🔙Назад в меню": "menu"}))
# Mailing handlers ends
