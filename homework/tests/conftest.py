import asyncio
from typing import AsyncGenerator
import pytest
from httpx import AsyncClient

from fastapi.testclient import TestClient
# from kombu.asynchronous.aws.connection import AsyncConnection
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, AsyncConnection
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from database import get_async_session
from models import Recipe

from main import app

# from python_advanced.module_26_fastapi.homework.tests.test_db_operations import client

#DATA BASE
DATABASE_URL_TEST = "sqlite+aiosqlite:///tests/test.db"

test_engine = create_async_engine(DATABASE_URL_TEST, echo=True) # тестовый движок
# переменная для ассинхронных сессий
test_async_session = sessionmaker(test_engine,
                                  expire_on_commit=False,
                                  class_=AsyncSession)
Recipe.metadata.bind = test_engine  # привязка метаданных к движку, для создания таблиц в тестовой БД

# сессию, которую в приложениие передавали через Depends,
# переопределяем для подключения к тестовой БД (возвр сессию)
async def override_get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with test_async_session() as session:
        yield session

app.dependency_overrides[get_async_session] = override_get_async_session

# Создание тестовой БД
# подключение к тестовой БД и использование метаданных для
# создания таблицы при начале тестирования
# В конце тестирования удаляем таблицу
@pytest.fixture(autouse=True, scope='session')
async def setup_database():
    print("fix_1 - async_db_connection start")
    async with test_engine.begin() as conn:
        await conn.run_sync(Recipe.metadata.create_all)

    yield test_engine

    async with test_engine.begin() as conn:
        print("fix_1 - async_db_connection finish")
        await conn.run_sync(Recipe.metadata.drop_all)


@pytest.fixture(scope='session')  # из документации для обработки асинх запросов
def event_loop(request):
    """
    Цикл обработки события по умолчанию
    """
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


#  Создаем клиента, который будет обращаться к эндпойнтам

@pytest.fixture(scope='session')
async def async_client() -> AsyncGenerator[AsyncClient, None]:
    # для тестирования асинхронного клиента
    print("fix_3 - async_client")
    async with AsyncClient(app=app, base_url="http://test") as async_client:
        yield async_client  # отдаем асинх клиента, чтобы он мог сделать запрос. Вызов из контекстного менеджера гарантирует закрытие после сессии (сессия - прогон всех тестов)

