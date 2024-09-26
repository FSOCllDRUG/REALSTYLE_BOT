from decimal import Decimal, InvalidOperation

from aiogram.filters import BaseFilter
from aiogram.types import Message


class IsDecimal(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        try:
            Decimal(message.text)
            return True
        except InvalidOperation:
            return False
