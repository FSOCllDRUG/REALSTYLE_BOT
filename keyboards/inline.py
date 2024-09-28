from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from tools.texts import manager_msg_url


async def get_callback_btns(
        *,
        btns: dict[str, str],
        sizes: tuple[int] = (2,)):
    keyboard = InlineKeyboardBuilder()

    for text, value in btns.items():
        if "://" in value:
            keyboard.add(InlineKeyboardButton(text=text, url=value))
        else:
            keyboard.add(InlineKeyboardButton(text=text, callback_data=value))

    return keyboard.adjust(*sizes).as_markup()


async def inline_main(admin: bool):
    inline = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Инструкция по БОТу 🤖",
                              url='https://telegra.ph/Instrukciya-po-ispolzovaniyu-bota-09-27-2')],
        [InlineKeyboardButton(text="💵Рассчитать стоимость", callback_data='calculate_cost')],
        [InlineKeyboardButton(text="🎯Отзывы", callback_data='reviews'),
         InlineKeyboardButton(text="📲Связь с менеджером", url=manager_msg_url)],
        [InlineKeyboardButton(text="🚚Как заказать?",
                              url='https://telegra.ph/Kak-polzovatsya-prilozheniem-POIZON-06-09'),
         InlineKeyboardButton(text="❓F.A.Q", callback_data='faq')],
        [InlineKeyboardButton(text="‼️Акции‼️", callback_data='discounts'),
         InlineKeyboardButton(text="🎒Товары в наличии", callback_data='in_stock')],
    ])
    if admin == True:
        inline.inline_keyboard.append([InlineKeyboardButton(text="💻Админ меню", callback_data='admin_menu')])
    return inline


inline_categories = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="👟Обувь/Верхняя одежда", callback_data='L')],
    [InlineKeyboardButton(text="👖Толстовка/Штаны", callback_data='M')],
    [InlineKeyboardButton(text="👕Футболка/Шорты", callback_data='S')],
    [InlineKeyboardButton(text="🧦Носки/Нижнее бельё", callback_data='XS')],
    [InlineKeyboardButton(text="📟Техника", callback_data='T')],
    [InlineKeyboardButton(text="Ⓜ️Меню", callback_data='menu')]
])

inline_cost = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="🔄Ещё расчёт", callback_data='calculate_cost'),
     InlineKeyboardButton(text="📦Заказать", url=f'{manager_msg_url}')],
    [InlineKeyboardButton(text="Ⓜ️Меню", callback_data='menu')]

])

admin_price = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Курс", callback_data='change_rate')],
    [InlineKeyboardButton(text="% страховка+выкуп", callback_data='change_insurance_redemption')],
    [InlineKeyboardButton(text="⬇️Обувь/Верхняя одежда⬇️", callback_data='nothing')],
    [InlineKeyboardButton(text="Доставка", callback_data='change_ship_L'),
     InlineKeyboardButton(text="Наценка", callback_data='change_margin_L')],
    [InlineKeyboardButton(text="⬇️Толстовка/Штаны⬇️", callback_data='nothing')],
    [InlineKeyboardButton(text="Доставка", callback_data='change_ship_M'),
     InlineKeyboardButton(text="Наценка", callback_data='change_margin_M')],
    [InlineKeyboardButton(text="⬇️Футболка/Шорты⬇️", callback_data='nothing')],
    [InlineKeyboardButton(text="Доставка", callback_data='change_ship_S'),
     InlineKeyboardButton(text="Наценка", callback_data='change_margin_S')],
    [InlineKeyboardButton(text="⬇️Носки/Нижнее бельё⬇️", callback_data='nothing')],
    [InlineKeyboardButton(text="Доставка", callback_data='change_ship_XS'),
     InlineKeyboardButton(text="Наценка", callback_data='change_margin_XS')],
    [InlineKeyboardButton(text="⬇️Техника⬇️", callback_data='nothing')],
    [InlineKeyboardButton(text="Доставка", callback_data='change_ship_T'),
     InlineKeyboardButton(text="Наценка", callback_data='change_margin_T')],
    [InlineKeyboardButton(text="Ⓜ️Вернутся в меню", callback_data='menu')]

])
