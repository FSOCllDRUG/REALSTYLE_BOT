from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from tools.texts import manager_msg_url, manager_order_msg_url, manager_express_msg_url


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
                              url="https://telegra.ph/Instrukciya-po-ispolzovaniyu-bota-09-27-2")],
        [InlineKeyboardButton(text="💵Рассчитать стоимость", callback_data="begin_calc")],
        [InlineKeyboardButton(text="🎯Отзывы", callback_data="reviews"),
         InlineKeyboardButton(text="📲Связь с менеджером", url=manager_msg_url)],
        [InlineKeyboardButton(text="🚚Как заказать?",
                              url="https://telegra.ph/Kak-polzovatsya-prilozheniem-POIZON-06-09"),
         InlineKeyboardButton(text="❓F.A.Q", callback_data="faq")],
        [InlineKeyboardButton(text="‼️Акции‼️", callback_data="discounts"),
         InlineKeyboardButton(text="🎒Товары в наличии", callback_data="in_stock")],
        [InlineKeyboardButton(text="🚄Экспресс-доставка", callback_data="express_delivery")],
    ])
    if admin == True:
        inline.inline_keyboard.append([InlineKeyboardButton(text="💻Админ меню", callback_data="admin_menu")])
    return inline


currency_list = [
    [InlineKeyboardButton(text="BYN🇧🇾", callback_data="BYN")],
    [InlineKeyboardButton(text="RUB🇷🇺", callback_data="RUB")],
    [InlineKeyboardButton(text="Меню", callback_data="menu")]
]

inline_currency = InlineKeyboardMarkup(inline_keyboard=currency_list)

categories_list = [
    [InlineKeyboardButton(text="👟Обувь", callback_data="shoes"),
     InlineKeyboardButton(text="👔Одежда", callback_data="clothes")],
    [InlineKeyboardButton(text="🕶/🧦Аксессуары", callback_data="accessories")],
    [InlineKeyboardButton(text="📟Техника", callback_data="tech")],
    [InlineKeyboardButton(text="⬅️Назад", callback_data="back_to_currency"),
     InlineKeyboardButton(text="Меню", callback_data="menu")]
]
inline_categories = InlineKeyboardMarkup(inline_keyboard=categories_list)


async def inline_subcategory_keyboard(category: str) -> InlineKeyboardMarkup:
    # 👞👟🥾🩴
    if category == "shoes":
        inline_keyboard = [
            [InlineKeyboardButton(text="👟Кроссовки", callback_data="sneakers"),
             InlineKeyboardButton(text="🥾Ботинки", callback_data="boots")],
            [InlineKeyboardButton(text="🩴Шлёпанцы", callback_data="slippers")],
        ]

    # 🧥🦺👖👕🩳
    elif category == "clothes":
        inline_keyboard = [
            [InlineKeyboardButton(text="🧥Верхняя одежда", callback_data="tops"),
             InlineKeyboardButton(text="🦺Худи", callback_data="hoodies")],
            [InlineKeyboardButton(text="👖Штаны", callback_data="pants"),
             InlineKeyboardButton(text="👕Футболки", callback_data="tShirts")],
            [InlineKeyboardButton(text="🩳Шорты", callback_data="shorts")],
        ]

    # 🧦🩲🌺⌚️🎒💼👝🧢💍🪢
    elif category == "accessories":
        inline_keyboard = [
            [InlineKeyboardButton(text="🧦Носки", callback_data="socks"),
             InlineKeyboardButton(text="👙Нижнее бельё", callback_data="panties")],
            [InlineKeyboardButton(text="🌺Парфюм", callback_data="perfume"),
             InlineKeyboardButton(text="⌚️Часы", callback_data="watches")],
            [InlineKeyboardButton(text="🎒Спортивные сумки", callback_data="sportBags"),
             InlineKeyboardButton(text="💼Большие сумки", callback_data="bigBags")],
            [InlineKeyboardButton(text="👝Маленькие сумки", callback_data="smallBags"),
             InlineKeyboardButton(text="🧢Кепки/Шапки", callback_data="hats")],
            [InlineKeyboardButton(text="💍Украшения", callback_data="jewelry"),
             InlineKeyboardButton(text="🪢Ремни", callback_data="belts")],
        ]

    # 🎧⌨🖱🖥
    elif category == "tech":
        inline_keyboard = [
            [InlineKeyboardButton(text="🎧Наушники", callback_data="headphones"),
             InlineKeyboardButton(text="⌨️Клавиатуры", callback_data="keyboard")],
            [InlineKeyboardButton(text="🖱️Мыши", callback_data="mouse"),
             InlineKeyboardButton(text="🖥Крупногабаритная техника", callback_data="computers")],
        ]

    else:
        inline_keyboard = [[InlineKeyboardButton(text="Меню", callback_data="menu")]]

    inline_keyboard.append([InlineKeyboardButton(text="⬅️Назад", callback_data="back_to_categories"),
                            InlineKeyboardButton(text="Меню", callback_data="menu")])

    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)


inline_cost = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="🔄Ещё расчёт", callback_data="begin_calc"),
     InlineKeyboardButton(text="📦Заказать", url=f"{manager_order_msg_url}")],
    [InlineKeyboardButton(text="Меню", callback_data="menu")]

])
admin_price = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Получить таблицу расценок", callback_data="get_config")],
    [InlineKeyboardButton(text="Получить отчёт о пользователях", callback_data="users_report")],
    [InlineKeyboardButton(text="Создать рассылку", callback_data="create_mailing")],
])

inline_express_delivery = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="👨‍💼Менеджер", url=f"{manager_express_msg_url}")],
    [InlineKeyboardButton(text="Меню", callback_data="menu")]

])