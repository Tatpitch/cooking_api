from pydantic import BaseModel, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class RunConfig(BaseModel):
    """
    Класс для хранения настроек запуска приложения
    """

    host: str = "0.0.0.0"
    port: int = 8000


# конфигурация для подключения к БД
class DatabaseConfig(BaseModel):
    # вся строка или можно было все по отдельности
    # (host, port, user, password, db_name)
    url: PostgresDsn
    # вместо строки для подключения используется валидация
    echo: bool = False
    echo_pool: bool = False
    pool_size: int = 5
    max_overflow: int = 10

    naming_convention: dict[str, str] = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_N_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }


class Settings(BaseSettings):
    """
    Класс длях ранения настроек приложения
    """

    model_config = SettingsConfigDict(
        env_file=(".env.template", ".env"),  # 2 файла для чтения параметров
        case_sensitive=False,  # нечувствительность к регистру
        env_nested_delimiter="__",  # разделитель для вложенных объектов
        env_prefix="APP_CONFIG__",
    )
    run: RunConfig = RunConfig()
    db: DatabaseConfig


settings = Settings()
