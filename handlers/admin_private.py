from decimal import Decimal

from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove

from create_bot import bot  # noqa
from filters.chat_type import ChatType
from filters.is_admin import IsAdmin
from filters.is_decimal import IsDecimal
from keyboards.inline import get_callback_btns, admin_price
from tools.config_manager import update_config_value
from tools.texts import admin_change_text

admin_private_router = Router()
admin_private_router.message.filter(ChatType("private"), IsAdmin())

config_readable = {
    "rate": "Курс 1¥",
    "insurance_redemption": "Страховка+выкуп",
    "ship_L": "Доставка(👟Обувь/Верхняя одежда)",
    "margin_L": "Наценка(👟Обувь/Верхняя одежда)",
    "ship_M": "Доставка(👖Толстовка/Штаны)",
    "margin_M": "Наценка(👖Толстовка/Штаны)",
    "ship_S": "Доставка(👕Футболка/Шорты)",
    "margin_S": "Наценка(👕Футболка/Шорты)",
    "ship_XS": "Доставка(🧦Носки/Нижнее бельё)",
    "margin_XS": "Наценка(🧦Носки/Нижнее бельё)",
}


class ChangeParam(StatesGroup):
    key = State()
    value = State()


@admin_private_router.callback_query(F.data == "admin_menu")
async def admin_menu(callback: CallbackQuery):
    await callback.answer("")
    await callback.message.answer(await admin_change_text(),
                                  reply_markup=admin_price
                                  )


@admin_private_router.callback_query(F.data.startswith("change_"), StateFilter(None))
async def change_param(callback: CallbackQuery, state: FSMContext):
    await callback.answer("")

    param = callback.data.replace("change_", "")
    await state.update_data(key=param)
    await callback.message.answer(f"Введите новое значение для {config_readable[param]}: ")
    await state.set_state(ChangeParam.value)


@admin_private_router.message(StateFilter(ChangeParam.value), IsDecimal())
async def change_param_value(message: Message, state: FSMContext):
    await state.update_data(value=Decimal(message.text))
    data = await state.get_data()
    key = data.get("key")
    value = data.get("value")
    await state.clear()
    await update_config_value(key, value)
    await message.answer(f"Параметр {config_readable[key]} изменен на {value:.2f} BYN",
                         reply_markup=ReplyKeyboardRemove(), )
    await message.answer("Что делаем дальше?",
                         reply_markup=await get_callback_btns(
                             btns={"💻Админ меню": "admin_menu", "Ⓜ️Меню": "menu"},
                         ))
