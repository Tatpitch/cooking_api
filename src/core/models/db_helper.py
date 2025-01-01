from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from core.config import settings


class DatabaseHelper:
    # инициализация асинхронного движка и фабрики асинхронных сессий
    def __init__(
        self,
        url: str,
        echo: bool = False,  # отображение запросов к БД
        echo_pool: bool = False,  # информация для connection pool
        pool_size: int = 5,  # кол-во открытых соединений
        max_overflow: int = 10,
    ) -> None:
        # создание асинхронного движка
        self.engine: AsyncEngine = create_async_engine(
            url=url,
            echo=echo,
            echo_pool=echo_pool,
            pool_size=pool_size,
            max_overflow=max_overflow,
        )
        # с аннотацией типов (создание фабрики сессий)
        self.session_factory: async_sessionmaker[AsyncSession] = (
            async_sessionmaker(
                bind=self.engine,  # движок
                autoflush=False,  # для асинх подключения
                autocommit=False,
                expire_on_commit=False,
            )
        )

    #  закрытие движка (соединения) - служебная ф-ия
    async def dispose(self) -> None:
        await self.engine.dispose()

    # создание и передача сессии в контекстном менеджере
    async def session_getter(
        self,
    ) -> AsyncGenerator[AsyncSession, None]:  # вместо dependes
        async with self.session_factory() as session:
            yield session


db_helper = DatabaseHelper(
    url=str(settings.db.url),  # преобразование объекта PostgresDsn в строку
    echo=settings.db.echo,
    echo_pool=settings.db.echo_pool,
    pool_size=settings.db.pool_size,
    max_overflow=settings.db.max_overflow,
)
