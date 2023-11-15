from sqlalchemy import create_engine,URL
from pydantic import BaseSettings
import pandas as pd
from rich.console import Console
console = Console()


class Settings(BaseSettings):
    DB_DIALECT : str = 'POSTGRES'
    DB_PORT: int
    DB_PASSWORD: str
    DB_USER: str
    DB_NAME: str
    DB_HOST: str
    DB_TABLE_NAME : str
    DB_CONNECTION_POOL_SIZE : int = 1
    class Config:
        env_file = 'database_env'


db_settings = Settings()
connection_string = URL.create(
    "postgresql+psycopg2",
    username=db_settings.DB_USER,
    password=db_settings.DB_PASSWORD,  # plain (unescaped) text
    host=db_settings.DB_HOST,
    database=db_settings.DB_NAME,
)
table_name=db_settings.DB_TABLE_NAME
engine = create_engine(connection_string,pool_size=db_settings.DB_CONNECTION_POOL_SIZE)
