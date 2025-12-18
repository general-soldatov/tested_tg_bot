from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message

from app.ai_router import router, config, session
from app.middleware import MiddleAI

def bases(func):
    def inner(*args, **kwargs):
        try:
            func(*args, **kwargs)
            print(*args, **kwargs)
        except Exception as e:
            print(e)
        finally:
            session.close()
    return inner

bot = Bot(config.tg.token)
dp = Dispatcher()
dp.update.middleware(MiddleAI())
dp.include_router(router)
# video = AnswerDB(session).count_video()

@bases
@dp.message(Command('start'))
async def start(message: Message):
    await message.answer(f'Hello, Dear {message.from_user.first_name}!')

if __name__ == "__main__":
    dp.run_polling(bot)