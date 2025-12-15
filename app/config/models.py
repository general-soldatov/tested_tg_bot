from pydantic import BaseModel

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