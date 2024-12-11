from pydantic import BaseModel
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)

class RunConfig(BaseModel):
    """
    Класс для хранения настроек запуска приложения
    """
    host: str = "0.0.0.0"
    port: int = 8000

class ApiPrefix(BaseModel):
    """
    класс для хранения префиксов роутеров
    """
    prefix: str = "/recipes"


class Settings(BaseSettings):
    """
    Класс длях ранения настроек приложения
    """
    run: RunConfig = RunConfig()
    api: ApiPrefix = ApiPrefix()


settings = Settings()