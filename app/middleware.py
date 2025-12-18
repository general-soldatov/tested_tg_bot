from aiogram import BaseMiddleware
from aiogram.types import Update
from aiogram.dispatcher.flags import get_flag
from typing import Dict, Any

from app.handler_question import Answers

class MiddleAI(BaseMiddleware):
    async def __call__(self, handler, event: Update, data: Dict[str, Any]):
        answer = Answers()
        data['category'] = answer(event.message.text)
        print(data['category'])
        return await handler(event, data)