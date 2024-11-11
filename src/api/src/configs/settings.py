import os
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict  # Updated import
from dotenv import load_dotenv

# Carregar o arquivo .env
load_dotenv()


class Settings(BaseSettings):
    DATABASE_URL: str
    SUPABASE_URL: str
    SUPABASE_KEY: str
    ACCESS_KEY_AWS: str
    SECRET_KEY_AWS: str
    SESSION_TOKEN_AWS: str

@lru_cache
def get_settings():
    return Settings()


settings = get_settings()
print("Environment variables loaded successfully: ",
      settings.model_dump())
