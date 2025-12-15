from app.config.config import Config

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

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, relationship
from app.database.models import Base, Videos

# Инициализируем движок и создаём таблицы
engine = create_engine(config.db.create_connect_alchemy())
Base.metadata.create_all(engine)

# Создаём сессию
Session = sessionmaker(bind=engine)
session = Session()

video = session.query(Videos).all()
print(video)

session.close()
