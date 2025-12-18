import re
from aiogram import Router
from aiogram.types import Message
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from app.database.models import Base
from app.config.config import Config

from app.database.models import Videos, Snapshots
# from app.middleware import MiddleAI
from app.filters import FilterAI

config = Config.model_validate_yaml("app/config/config.yaml")

router = Router()
# router.message.middleware(MiddleAI())

# Инициализируем движок и создаём таблицы
engine = create_engine(config.db.create_connect_alchemy())
Base.metadata.create_all(engine)
# Создаём сессию
Session = sessionmaker(bind=engine)
session = Session()


@router.message(FilterAI('all_video'))
async def all_video(message: Message, category: str):
    result = session.query(func.count(Videos.id)).scalar()
    await message.answer(str(result))

@router.message(FilterAI('more_views'))
async def more_views(message: Message, category: str):
    match = re.search(r'(?<=е\s)\d+(?:\s\d+)?', message.text)
    count = int(match.group().replace(' ', '').replace('е', ''))
    result = session.query(func.count(Videos.id)).where(
        Videos.views_count > count).scalar()
    await message.answer(str(result))