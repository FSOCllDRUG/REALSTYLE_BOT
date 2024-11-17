from decimal import Decimal

from tools.config_manager import get_config_value, read_config

manager_msg_url = "https://t.me/realstyle_manager?text=%D0%97%D0%B4%D1%80%D0%B0%D0%B2%D1%81%D1%82%D0%B2%D1%83%D0%B9%D1%82%D0%B5%21%0A%D0%AF%20%D1%85%D0%BE%D1%82%D0%B5%D0%BB%28%D0%B0%29%20%D0%B1%D1%8B%20%D1%83%D0%B7%D0%BD%D0%B0%D1%82%D1%8C%2C%20"
manager_order_msg_url = "https://t.me/realstyle_manager?text=%D0%9F%D1%80%D0%B8%D0%B2%D0%B5%D1%82%21%0A%D0%AF%20%D1%85%D0%BE%D1%87%D1%83%20%D0%BE%D1%84%D0%BE%D1%80%D0%BC%D0%B8%D1%82%D1%8C%20%D0%B7%D0%B0%D0%BA%D0%B0%D0%B7%2C%20"
manager_express_msg_url = ("https://t.me/realstyle_manager?text=%D0%9F%D1%80%D0%B8%D0%B2%D0%B5%D1%82%21%0A%D0%A5%D0%BE%D1%87%D1%83%20%D1%83%D0%B7%D0%BD%D0%B0%D1%82%D1%8C%20%D0%BE%20%D1%8D%D0%BA%D1%81%D0%BF%D1%80%D0%B5%D1%81%D1%81-%D0%B4%D0%BE%D1%81%D1%82%D0%B0%D0%B2%D0%BA%D0%B5")


async def cost_text(cost_data: dict):
    # Выбранная валюта из диалога(FSM)
    currency = cost_data.get("currency")
    # Цена товара из диалога(FSM)
    price = Decimal(cost_data.get("price"))
    # Курс в выбранной валюте
    rate = Decimal(await get_config_value(f"rate_{currency}"))
    # Цена товара на Poizon
    cost_poizon = price * rate
    # Категория товара(подкатегория)
    category = cost_data.get("subcategory")
    print(category)
    # Доставка вещи выбранной категории
    ship = Decimal(await get_config_value(f"ship_{category}_{currency}"))
    # Комиссия сервиса
    margin = Decimal(await get_config_value(f"margin_{category}_{currency}"))
    # Процент страховки
    insurance = Decimal(await get_config_value("insurance"))
    # Финальная стоимость = Цена на Poizon + Доставка + Комиссия сервиса + Страховка
    final_cost = cost_poizon + ship + margin + cost_poizon / 100 * insurance
    if currency == "RUB":
        footer = (
            "<i>Срок доставки до склада в Москве 9-14 дней. Отправляем товары в ваши города СДЭКОМ или Boxberry.\n\n"
            "По всем вопросам и оформлению заказа писать нашему менеджеру - @realstyle_manager</i>.")
    else:
        footer = (
            "<i>Срок доставки до склада в Минске 15-20 дней. Отправляем товары в ваши города ЕВРОПОЧТОЙ"
            " или любой другой транспортной компанией.\n\n"
            "По всем вопросам и оформлению заказа писать нашему менеджеру - @realstyle_manager</i>.")
    return (f"Ваш расчёт заказа:\n\n"
            f"- Курс ¥ = {rate:.2f} {currency}\n"
            f"- Цена товара на Poizon: {cost_poizon:.2f} {currency}\n"
            f"- Доставка до склада в Минске: {ship:.2f} {currency}\n"
            f"- Комиссия сервиса: {margin:.2f} {currency}\n"
            f"- Страховка: {cost_poizon / 100 * insurance:.2f} {currency}"
            f"\n\n<b>Итоговая стоимость: {final_cost:.2f} {currency}</b>\n\n"
            f"{footer}")


async def admin_change_text():
    config = await read_config()
    return (f"Админ панель\n\n"
            f"Курс 1¥ = {config['rate']} BYN\n"
            f"%(процент) страховки - {config['insurance_redemption']}%\n\n"

            f"Формула цены:\n"
            f"<blockquote expandable> стоимость = цена * курс * ((100 + страховка_выкуп) / 100) + доставка + наценка</blockquote>"
            f"\n\n"
            f"Выбери ниже, что ты хочешь изменить")
