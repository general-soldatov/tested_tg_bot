from aiogram.filters import BaseFilter
from aiogram.types import Message

class FilterAI(BaseFilter):
    def __init__(self, command: str) -> None:
        self.command = command

    async def __call__(self, message: Message, category: str):
        return category == self.command