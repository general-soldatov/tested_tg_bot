import yaml
from typing import List, Dict
from pydantic import BaseModel
from app.config.db import DB

class YamlProject(BaseModel):
    @classmethod
    def model_validate_yaml(cls, path, encoding='utf-8'):
        with open(path, 'r', encoding=encoding) as file:
            data = yaml.safe_load(file.read())
            return cls.model_validate(data)

class Config(YamlProject):
    db: DB
