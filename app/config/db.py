from pydantic import BaseModel

class DB(BaseModel):
    database: str
    user: str
    password: str
    host: str
    port: str