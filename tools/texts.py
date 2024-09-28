from decimal import Decimal

from tools.config_manager import get_config_value, read_config

manager_msg_url = "https://t.me/realstyle_manager?text=%D0%97%D0%B4%D1%80%D0%B0%D0%B2%D1%81%D1%82%D0%B2%D1%83%D0%B8%CC%86%D1%82%D0%B5%21%0A%D0%AF%20%D1%85%D0%BE%D1%82%D0%B5%D0%BB%20%D0%B1%D1%8B%20%D1%83%D0%B7%D0%BD%D0%B0%D1%82%D1%8C%2C%20"
manager_order_msg_url = "https://t.me/realstyle_manager?text=%D0%9F%D1%80%D0%B8%D0%B2%D0%B5%D1%82%21%0A%D0%AF%20%D1%85%D0%BE%D1%87%D1%83%20%D0%BE%D1%84%D0%BE%D1%80%D0%BC%D0%B8%D1%82%D1%8C%20%D0%B7%D0%B0%D0%BA%D0%B0%D0%B7%2C%20"


async def cost_text(cost: Decimal):
    rate = await get_config_value("rate")
    return (f"Стоимость товара: {cost:.2f} BYN\n\n"
            f"Стоимость в себя включает:↙️\n"
            f"- Доставка по Китаю\n"
            f"- Доставка Китай-Минск\n"
            f"Комиссия нашего сервиса\n"
            f"Курс ¥ - {rate} BYN\n\n"
            f"Стоимость рассчитана до склада в Минске.\n"
            f"В стоимость не включена страховка,"
            f"данную функцию можно включить при "
            f"оформлении заказа, "
            f"менеджер обязательно уточнит это.\n\n"
            f"‼️При оформлении от 10-ти позиций "
            f"индивидуальная скидка‼️\n"
            f"Уточняйте тут: @realstyle_manager")


async def admin_change_text():
    config = await read_config()
    return (f"Админ панель\n\n"
            f"Курс 1¥ = {config['rate']} BYN\n"
            f"Страховка+выкуп - {config['insurance_redemption']}%\n\n"
            f"👟Обувь/Верхняя одежда\n"
            f"Доставка— {config['ship_L']} BYN\n"
            f"Наценка— {config['margin_L']} BYN\n"
            f"👖Толстовка/Штаны\n"
            f"Доставка— {config['ship_M']} BYN\n"
            f"Наценка— {config['margin_M']} BYN\n"
            f"👕Футболка/Шорты\n"
            f"Доставка— {config['ship_S']} BYN\n"
            f"Наценка— {config['margin_S']} BYN\n"
            f"🧦Носки/Нижнее бельё\n"
            f"Доставка— {config['ship_XS']} BYN\n"
            f"Наценка— {config['margin_XS']} BYN\n"
            f"📟Техника\n"
            f"Доставка— {config['ship_T']} BYN\n"
            f"Наценка— {config['margin_T']} BYN\n\n\n"
            f"Формула:\n"
            f"<blockquote expandable> стоимость = цена * курс * ((100 + страховка_выкуп) / 100) + доставка + наценка</blockquote>"
            f"\n\n"
            f"Выбери ниже, что ты хочешь изменить")
