from pydantic import BaseModel
from pydantic import PostgresDsn
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

# конфигурация для подключения к БД
class DatabaseConfig(BaseModel):
    url: PostgresDsn        # вся строка или можно было все по отдельности (host, port, user, password, db_name)
    # вместо строки для подключения используется валидация, содержащая набор разрешенных и запрещенных ссылок
    echo: bool = False
    echo_pool: bool = False
    pool_size: int = 50
    max_overflow: int = 10


class Settings(BaseSettings):
    """
    Класс длях ранения настроек приложения
    """
    run: RunConfig = RunConfig()
    api: ApiPrefix = ApiPrefix()
    db: DatabaseConfig


settings = Settings()