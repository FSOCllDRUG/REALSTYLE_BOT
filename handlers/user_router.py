from decimal import Decimal

from aiogram import Router, F  # noqa
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove  # noqa

from create_bot import bot, env_admins  # noqa
from filters.is_decimal import IsDecimal
from keyboards.inline import inline_main, inline_categories, inline_cost, get_callback_btns
from keyboards.reply import reply_menu # noqa
from tools.config_manager import get_config_value
from tools.cost_calculation import calculate_cost
from tools.texts import cost_text, manager_msg_url

user_router = Router()


@user_router.message(StateFilter("*"), F.text.casefold() == "отмена")
async def cancel_fsm(message: Message, state: FSMContext):
    await state.clear()
    photo_id = 'AgACAgIAAxkBAAIDbGb2Am8MuNKnVDEg-ZjGycSiZ5TXAAKo4zEbh86xSywUjO7c1sMIAQADAgADeQADNgQ'
    text = ("Действие отменено!\n\n<b>Я бот помощник</b> @realstyle_by\n"
            "Помогу рассчитать тебе стоимость товара с <b>POIZON</b> и не только 🤖")
    await message.answer_photo(photo_id, caption=text, reply_markup=await inline_main(message.from_user.id
                                                                                      in env_admins))


@user_router.callback_query(F.data == "nothing")
async def nothing(callback: CallbackQuery):
    await callback.answer("Это декоративная кнопошка, ничего не делаю")


@user_router.message(CommandStart())
async def cmd_start(message: Message):
    photo_id = 'AgACAgIAAxkBAAIDbGb2Am8MuNKnVDEg-ZjGycSiZ5TXAAKo4zEbh86xSywUjO7c1sMIAQADAgADeQADNgQ'
    text = ("<b>Привет! Я бот помощник</b> @realstyle_by\n"
            "Помогу рассчитать тебе стоимость товара с <b>POIZON</b> и не только 🤖")
    await message.answer_photo(photo_id, caption=text, reply_markup=ReplyKeyboardRemove())
    await message.answer(
        f"C моей помощью ты можешь:\n"
        f"- Рассчитать сумму своего заказа💵\n"
        f"- Получить ответы на вопросы🧐\n"
        f"- Связаться с менеджером📲",
        reply_markup=await inline_main(message.from_user.id in env_admins)
    )


@user_router.callback_query(F.data == "menu")
async def main_menu_inline(callback: CallbackQuery, state: FSMContext):
    await callback.answer("")
    await state.clear()
    photo_id = 'AgACAgIAAxkBAAIDbGb2Am8MuNKnVDEg-ZjGycSiZ5TXAAKo4zEbh86xSywUjO7c1sMIAQADAgADeQADNgQ'
    text = ("<b>Привет! Я бот помощник</b> @realstyle_by\n"
            "Помогу рассчитать тебе стоимость товара с <b>POIZON</b> и не только 🤖")
    await callback.message.answer_photo(photo_id, caption=text, reply_markup=await inline_main(callback.from_user.id
                                                                                               in env_admins))


@user_router.message(F.text == "Меню")
async def main_menu_reply(message: Message, state: FSMContext):
    await state.clear()
    photo_id = 'AgACAgIAAxkBAAIDbGb2Am8MuNKnVDEg-ZjGycSiZ5TXAAKo4zEbh86xSywUjO7c1sMIAQADAgADeQADNgQ'
    text = ("<b>Привет! Я бот помощник</b> @realstyle_by\n"
            "Помогу рассчитать тебе стоимость товара с <b>POIZON</b> и не только 🤖")
    await message.answer_photo(photo_id, caption=text, reply_markup=await inline_main(message.from_user.id
                                                                                      in env_admins))


class CostCalc(StatesGroup):
    category = State()
    price = State()


@user_router.callback_query(F.data == "calculate_cost")
async def choose_category(callback: CallbackQuery, state: FSMContext):
    await callback.answer("")
    await callback.message.answer("Выбери категорию:", reply_markup=inline_categories)
    await state.set_state(CostCalc.category)


@user_router.callback_query(F.data.in_({"L", "M", "S", "XS", "T"}), StateFilter(CostCalc.category))
async def category_chosen(callback: CallbackQuery, state: FSMContext):
    await callback.answer("")
    await state.update_data(category=callback.data)
    rate = await get_config_value("rate")
    photo_id = 'AgACAgIAAxkBAAIDSGb19ZiQF91MJ8Yip0Xb7zyIaFzZAAKN4zEbh86xSzW2ZcFARwGPAQADAgADeAADNgQ'
    text = (f"Введи цену в ¥(Юанях), а я рассчитаю итоговую стоимость.\n\n"
            f"Актуальный курс— 1¥ = {rate} BYN")
    await callback.message.answer_photo(photo_id, caption=text)
    await state.set_state(CostCalc.price)


@user_router.message(StateFilter(CostCalc.price), IsDecimal())
async def category_price(message: Message, state: FSMContext):
    await state.update_data(price=Decimal(message.text))
    data = await state.get_data()
    price = data.get("price")
    category = data.get("category")
    cost = await calculate_cost(price, category)
    await state.clear()
    await message.answer(f"{await cost_text(cost)}", reply_markup=inline_cost)


@user_router.callback_query(F.data == "in_stock")
async def in_stock(callback: CallbackQuery):
    await callback.answer("")
    photo_id = "AgACAgIAAxkBAAICyWb1rORmEizavfFFqTplw9wBxzw8AAJd4jEbh86xS617MVj75uY1AQADAgADeQADNgQ"
    text = ("<b>Вы можете приобрести товары, которые уже имеются в наличии на нашем складе.</b> "
            "🥰\n\n"
            "Все товары из наличия представлены в нашем инстаграме\n\n"
            "➖ <b>Товары представленные в</b> <i>актуальных «НА РУКАХ✅»</i> , <b>мы закупаем в "
            "Европе и "
            "Китае.</b>\n"
            "➖ <b>Все товары из наличия, проходят тщательную проверку на оригинальность и "
            "качество.</b>\n"
            "➖ <b>Доставка товаров из наличия, составляет от 2, до 5 рабочих дней.</b>!")
    await callback.message.answer_photo(photo_id, caption=text, reply_markup=await get_callback_btns(btns={"НА РУКАХ✅":
                                                                                                               "https://www.instagram.com/s/aGlnaGxpZ2h0OjE3OTE4MjM3ODY3ODAzMzAx?igsh=MTI4cHo1cHRqemR2OQ",
                                                                                                           "Наш "
                                                                                                           "Instagram": "https://www.instagram.com/realstyle_by/",
                                                                                                           "🔙Назад": "menu"}))


@user_router.callback_query(F.data == "discounts")
async def discount(callback: CallbackQuery):
    await callback.answer("")
    await callback.message.answer("<b>Постоянная акция!</b> 😇\n\n"
                                  "<b>При оформлении 2-х и более, товаров за один раз, стоимость каждого следующего "
                                  "товара будет идти со скидкой.</b>\n\n"
                                  "👟 На обувь: <b>Минус 20 BYN</b>\n"
                                  "👖 На толстовки/штаны: <b>Минус 15 BYN</b>\n"
                                  "👕 На футболки/шорты: <b>Минус 15 BYN</b>\n"
                                  "🧦 На носки/нижнее белье: <b>Минус 5 BYN</b>\n\n"
                                  "<b>При оформлении 10-ти позиций и более скидка обсуждается индивидуально с "
                                  "менеджером‼️</b>\n\n"
                                  "По всем вопросам обращайтесь к менеджеру⬇️",
                                  reply_markup=await get_callback_btns(btns={"Менеджер": f"{manager_msg_url}",
                                                                             "🔙Назад": "menu"}, sizes=(1,)))


@user_router.callback_query(F.data == "reviews")
async def faq(callback: CallbackQuery):
    await callback.answer("")
    await callback.message.answer("Отзывы наших клиентов:", reply_markup=await get_callback_btns(
        btns={"Отзывы": "https://www.instagram.com/s/aGlnaGxpZ2h0OjE3OTY2NDIwNTEwMjEyMjQ0", "🔙Назад": "menu"},
        sizes=(1,)))


@user_router.callback_query(F.data == "faq")
async def faq(callback: CallbackQuery):
    await callback.answer("")
    await callback.message.answer("У тебя возникли вопросы по работе с ботом?\n"
                                  "На этот случай у нас есть сайт со статьями, которые помогут тебе.\n\n"
                                  'Нажми на кнопку "INFO" в левом нижнем углу экрана\n'
                                  "⬇️")

# @user_router.message(F.photo)
# async def get_photo_id(message: Message):
#     photo_id = message.photo[-1].file_id
#     await message.answer(f"id фотографии:\n<pre>{photo_id}</pre>")
# AgACAgIAAxkBAAIDSGb19ZiQF91MJ8Yip0Xb7zyIaFzZAAKN4zEbh86xSzW2ZcFARwGPAQADAgADeAADNgQ
