from app.config.config import Config
from app.database.handler import AnswerDB

config = Config.model_validate_yaml("app/config/config.yaml")
# try:
#     connection = psycopg2.connect(config.db.create_connect())
#     print("Подключение успешно установлено!")
# except Exception as e:
#     print(f"Ошибка подключения: {e}")
# finally:
#     if connection:
#         connection.close()
#     print("Соединение закрыто.")

from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker, relationship
from app.database.models import Base, Videos, Snapshots
from datetime import date

# Инициализируем движок и создаём таблицы
engine = create_engine(config.db.create_connect_alchemy())
Base.metadata.create_all(engine)

# Создаём сессию
Session = sessionmaker(bind=engine)
session = Session()

video = AnswerDB(session).count_video()

# video = session.query(func.sum(Snapshots.delta_views_count).label('total')).filter(
#     func.date(Snapshots.created_at) == date(2025, 11, 28),
#     Snapshots.delta_views_count > 0).scalar()

print((video))

session.close()
