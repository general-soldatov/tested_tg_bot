import yaml
from typing import List, Dict
from pydantic import BaseModel

class YamlProject(BaseModel):
    @classmethod
    def model_validate_yaml(cls, path, encoding='utf-8'):
        with open(path, 'r', encoding=encoding) as file:
            data = yaml.safe_load(file.read())
            return cls.model_validate(data)

class DB(BaseModel):
    database: str
    user: str
    password: str
    host: str
    port: str

    def create_connect(self):
        return f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"

    def create_connect_alchemy(self):
        return f"postgresql+psycopg2://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"

class Config(YamlProject):
    db: DB
