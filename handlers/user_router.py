from decimal import Decimal

from aiogram import Router, F  # noqa
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove  # noqa

from create_bot import bot, env_admins  # noqa
from filters.is_decimal import IsDecimal
from keyboards.inline import inline_main, inline_categories, inline_cost, get_callback_btns, inline_currency, \
    inline_subcategory_keyboard, inline_express_delivery
from keyboards.reply import reply_menu  # noqa
from tools.config_manager import get_config_value
from tools.texts import cost_text, manager_msg_url
from tools.users import add_user

user_router = Router()


@user_router.message(StateFilter("*"), F.text.casefold() == "отмена")
async def cancel_fsm(message: Message, state: FSMContext):
    await state.clear()
    photo_id = 'AgACAgIAAxkBAAIX-Wc5B2eB0DFMY8J63VpEytimy-_NAAJD5DEbuLvJSSfKeC2M2YTTAQADAgADeAADNgQ'
    text = ("Действие отменено!\n\n<b>Я бот помощник</b> @realstyle_by\n"
            "Помогу рассчитать тебе стоимость товара с <b>POIZON</b> и не только 🤖")
    await message.answer_photo(photo_id, caption=text, reply_markup=await inline_main(message.from_user.id
                                                                                      in env_admins))


@user_router.callback_query(F.data == "nothing")
async def nothing(callback: CallbackQuery):
    await callback.answer("Это декоративная кнопошка, ничего не делаю")


@user_router.message(CommandStart())
async def cmd_start(message: Message):
    await add_user(message.from_user.id)
    photo_id = 'AgACAgIAAxkBAAIX-Wc5B2eB0DFMY8J63VpEytimy-_NAAJD5DEbuLvJSSfKeC2M2YTTAQADAgADeAADNgQ'
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
    photo_id = 'AgACAgIAAxkBAAIX-Wc5B2eB0DFMY8J63VpEytimy-_NAAJD5DEbuLvJSSfKeC2M2YTTAQADAgADeAADNgQ'
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
    currency = State()
    category = State()
    subcategory = State()
    price = State()


@user_router.callback_query(F.data == "back_to_currency", StateFilter(CostCalc.category))
@user_router.callback_query(F.data == "begin_calc")
async def choose_currency(callback: CallbackQuery, state: FSMContext):
    await callback.answer("")
    await callback.message.answer("Выбери валюту:", reply_markup=inline_currency)
    await state.set_state(CostCalc.currency)


@user_router.callback_query(F.data == "back_to_categories", StateFilter(CostCalc.subcategory))
@user_router.callback_query(F.data.in_({"BYN", "RUB"}))
async def choose_category(callback: CallbackQuery, state: FSMContext):
    await callback.answer("")
    if callback.data == "BYN" or callback.data == "RUB":
        await state.update_data(currency=callback.data)
    await callback.message.answer("Выбери категорию:", reply_markup=inline_categories)
    await state.set_state(CostCalc.category)


@user_router.callback_query(F.data.in_({"clothes", "shoes", "accessories", "tech"
                                        }), StateFilter(CostCalc.category))
async def choose_subcategory(callback: CallbackQuery, state: FSMContext):
    await callback.answer("")
    await state.update_data(category=callback.data)
    await callback.message.answer("Выбери подкатегорию:",
                                  reply_markup=await inline_subcategory_keyboard(callback.data))
    await state.set_state(CostCalc.subcategory)


@user_router.callback_query(F.data.in_({'sneakers', 'boots', 'slippers',  # shoes
                                        'tops', 'hoodies', 'pants', 'tShirts', 'shorts',  # clothes
                                        'socks', 'panties', 'perfume', 'watches', 'sportBags', 'bigBags',
                                        'smallBags', 'hats', 'jewelry', 'belts',  # accessories
                                        'headphones', 'keyboard', 'mouse', 'computers'  # tech
                                        }), StateFilter(CostCalc.subcategory))
async def subcategory_chosen(callback: CallbackQuery, state: FSMContext):
    await callback.answer("")
    await state.update_data(subcategory=callback.data)
    data = await state.get_data()
    currency = data.get("currency")
    print(data)
    rate = await get_config_value(f"rate_{currency}")
    photo_id = 'AgACAgIAAxkBAAIDSGb19ZiQF91MJ8Yip0Xb7zyIaFzZAAKN4zEbh86xSzW2ZcFARwGPAQADAgADeAADNgQ'
    text = (f"Введи цену в ¥(Юанях), а я рассчитаю итоговую стоимость.\n\n"
            f"Актуальный курс 1¥ = {rate} {currency}")
    await callback.message.answer_photo(photo_id, caption=text)
    await state.set_state(CostCalc.price)


@user_router.message(StateFilter(CostCalc.price), IsDecimal())
async def category_price(message: Message, state: FSMContext):
    await state.update_data(price=Decimal(message.text))
    cost_data = await state.get_data()
    # price = data.get("price")
    # currency = data.get("currency")
    # subcategory = data.get("subcategory")
    # cost = await calculate_cost(price, subcategory, currency)

    await state.clear()
    await message.answer(f"{await cost_text(cost_data)}", reply_markup=inline_cost)

@user_router.callback_query(F.data == "exoress_delivery")
async def exoress_delivery(callback: CallbackQuery):
    await callback.answer("")
    await callback.message.answer("<b>Индивидуальный расчёт экспресс-доставки (5-7 дней) можно получить у менеджера</b>",
                                  reply_markup=inline_express_delivery)

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


@user_router.message(F.text == "/dev")
async def developer_info(message: Message):
    await message.answer(f"Контакты👨🏻‍💻:\n"
                         f"Telegram: <b><i><u><a href='tg://user?id=6092344340'>НАПИСАТЬ</a></u></i></b>\n")

# @user_router.message(F.photo)
# async def get_photo_id(message: Message):
#     photo_id = message.photo[-1].file_id
#     await message.answer(f"id фотографии:\n<pre>{photo_id}</pre>")
