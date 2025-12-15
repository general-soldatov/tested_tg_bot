import psycopg2
from app.config.model import Config

config = Config.model_validate_yaml("app/config/config.yaml")
try:
    connection = psycopg2.connect(**config.db.model_dump())
    print("Подключение успешно установлено!")
except Exception as e:
    print(f"Ошибка подключения: {e}")
finally:
    if connection:
        connection.close()
    print("Соединение закрыто.")
