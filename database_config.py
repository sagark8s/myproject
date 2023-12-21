from sqlalchemy import URL
from pydantic_settings import BaseSettings
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
def table_name():
    return db_settings.DB_TABLE_NAME
def load_conn():
    connection_string = URL.create(
        "postgresql+psycopg2",
        username=db_settings.DB_USER,
        password=db_settings.DB_PASSWORD,  # plain (unescaped) text
        host=db_settings.DB_HOST,
        database=db_settings.DB_NAME,
    )
    return connection_string
base_ip = "127.0.0.1:8512"
main_table_name=db_settings.DB_TABLE_NAME
faq_table_name="stb_vector_faq_store"
    #http://127.0.0.1:8512/generate_map/?c=-4.3478359,55.83289869999999&name=vishnu
    #'20.193.133.240:8518'

# engine = create_engine(connection_string,pool_size=db_settings.DB_CONNECTION_POOL_SIZE)
