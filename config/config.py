from pydantic_settings import BaseSettings
from pydantic import EmailStr


''' DB settings for common database and config database'''
class Settings(BaseSettings):
    DB_DIALECT : str
    DB_PORT: int
    DB_PASSWORD: str
    DB_USER: str
    DB_NAME: str
    DB_HOST: str
    CONFIG_DB : str

    EMAIL_HOST: str
    EMAIL_PORT: int
    EMAIL_USERNAME: str
    EMAIL_PASSWORD: str
    EMAIL_FROM: EmailStr


    class Config:
        env_file = 'config/env'


settings = Settings()
