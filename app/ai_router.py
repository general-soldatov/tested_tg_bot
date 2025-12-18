import re
from aiogram import Router
from aiogram.types import Message
from datetime import datetime
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from app.database.models import Base
from app.config.config import Config
from app.database.models import Videos, Snapshots
from app.filters import FilterAI
import locale

locale.setlocale(locale.LC_TIME, "ru_RU.UTF-8")

config = Config.model_validate_yaml("app/config/config.yaml")

router = Router()

engine = create_engine(config.db.create_connect_alchemy())
Base.metadata.create_all(engine)
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

@router.message(FilterAI('less_views'))
async def less_views(message: Message, category: str):
    match = re.search(r'(?<=е\s)\d+(?:\s\d+)?', message.text)
    count = int(match.group().replace(' ', '').replace('е', ''))
    result = session.query(func.count(Videos.id)).where(
        Videos.views_count < count).scalar()
    await message.answer(str(result))

@router.message(FilterAI('new_views_video'))
async def new_views_video(message: Message, category: str):
    date_pattern = r'\d{1,2} \w+ \d{4}'
    match = re.search(date_pattern, message.text)
    date_str = match.group()
    date_obj = datetime.strptime(date_str, '%d %B %Y')
    result = session.query(Snapshots.video_id).order_by(Snapshots.video_id.desc()).filter(
            func.date(Snapshots.created_at) == date_obj.date(),
            Snapshots.delta_views_count > 0).count()
    await message.answer(str(result))

@router.message(FilterAI('products_of_creator'))
async def products_of_creator(message: Message, category: str):
    id_ = re.search(r'id (\w+)', message.text).group().replace("id ", '')
    date_str = re.search(r'с (\d{1,2} \w+ \d{4})', message.text).group()
    date_obj_1 = datetime.strptime(date_str.replace('с ', ''), '%d %B %Y').date()
    date_str = re.search(r'по (\d{1,2} \w+ \d{4})', message.text).group()
    date_obj_2 = datetime.strptime(date_str.replace('по ', ''), '%d %B %Y').date()
    result = session.query(Videos.id).filter(Videos.creator_id == id_,
                                    Videos.created_at.between(date_obj_1, date_obj_2)).count()
    await message.answer(str(result))

@router.message(FilterAI('count_video'))
async def count_video(message: Message, category: str):
    match = re.search(r'\d{1,2} \w+ \d{4}', message.text)
    date_obj = datetime.strptime(match.group(), '%d %B %Y').date()
    result = session.query(func.sum(Snapshots.delta_views_count).label('total')).filter(
            func.date(Snapshots.created_at) == date_obj,
            Snapshots.delta_views_count > 0).scalar()
    if not result:
        result = 0
    await message.answer(str(result))