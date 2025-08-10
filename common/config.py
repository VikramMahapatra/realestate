
from pydantic import BaseSettings
import os

class Settings(BaseSettings):
    SERVICE_NAME: str = os.getenv('SERVICE_NAME', 'service')
    DATABASE_URL: str = os.getenv('DATABASE_URL', 'postgresql+psycopg2://user:pass@db:5432/appdb')
    JWT_SECRET: str = os.getenv('JWT_SECRET', 'supersecretjwt')
    JWT_ALGORITHM: str = os.getenv('JWT_ALGORITHM', 'HS256')
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60*24*7
settings = Settings()
