from typing import List
from datetime import datetime, date
from app.config.config import Config
from app.config.models import Video, VideosModel, SnapshotsModel
from app.database.models import Videos, Snapshots
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker, relationship
from app.database.models import Base, Videos

def load_info_video() -> List[VideosModel]:
    with open('app/static/videos.json', encoding='utf-8') as file:
        obj = Video.model_validate_json(file.read())
        return obj.videos

# Инициализируем движок и создаём таблицы
config = Config.model_validate_yaml("app/config/config.yaml")
engine = create_engine(config.db.create_connect_alchemy())
Base.metadata.create_all(engine)

# Создаём сессию
Session = sessionmaker(bind=engine)
session = Session()

def load_to_db():
    for video in load_info_video():
        new_video = Videos(**video.model_dump())
        session.add(new_video)
        session.commit()
        for snapshot in video.snapshots:
            new_snapshot = Snapshots(**snapshot.model_dump())
            session.add(new_snapshot)
            session.commit()

def check_video():
    video = session.query(Videos).filter(func.date(Videos.video_created_at) == date(2025, 11, 28)).all()
    print(VideosModel.model_validate(video[0].__dict__))

def check_snap():
    videos = session.query(Snapshots).filter(func.date(Snapshots.created_at) == date(2025, 11, 28)).count()
    print(videos)

# load_to_db()
# check_video()
check_snap()

session.close()