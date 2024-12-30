import asyncio
from typing import AsyncGenerator
from collections.abc import AsyncGenerator
import pytest_asyncio
import pytest
from httpx import AsyncClient, ASGITransport

from fastapi.testclient import TestClient
# from kombu.asynchronous.aws.connection import AsyncConnection
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncEngine,
    async_sessionmaker,
    AsyncSession,
)
from sqlalchemy.pool import NullPool
from sqlalchemy.orm import DeclarativeBase
# from sqlalchemy.orm import sessionmaker
from sqlalchemy import insert
from core.models.base import Base
from core.models.db_helper import db_helper
from core.models.ingredient import Ingredient
from core.models.recipe import Recipe
from core.models.ingredient_in_recipe import IngredientsInRecipe
from main import main_app


#DATA BASE
DATABASE_URL_TEST = "sqlite+aiosqlite:///tests/test.db"
# DATABASE_URL_TEST = "postgresql+asyncpg://test:test@localhost:543322/test"

test_engine = create_async_engine(DATABASE_URL_TEST, echo=True) # тестовый движок
# переменная для ассинхронных сессий
test_async_session = async_sessionmaker(test_engine,
                                  expire_on_commit=False)
# Base.metadata.bind = test_engine  # привязка метаданных к движку, для создания таблиц в тестовой БД ???

# сессию, которую в приложениие передавали через Depends,
# переопределяем для подключения к тестовой БД (возвр сессию)
async def override_get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with test_async_session() as session:
        yield session

main_app.dependency_overrides[db_helper.session_getter] = override_get_async_session

# client = TestClient(main_app)

# Данные для тестовой базы данных
ingredients = [
    {
        "ingredient_name": "Test ingredient 1",
        "ingredient_description": "Test ingredient description 1",
        },
    {
        "ingredient_name": "Test ingredient 2",
        "ingredient_description": "Test ingredient description 2",
        },
    {
        "ingredient_name": "Test ingredient 3",
        "ingredient_description": "Test ingredient description 3",
        },
    ]

recipes = [
    {
        "recipe_name": "Test recipe 1",
        "cooking_time": 20,
        "count_views": 5,
        "recipe_description": "Test recipe description 1",
        },
    {
        "recipe_name": "Test recipe 2",
        "cooking_time": 40,
        "count_views": 7,
        "recipe_description": "Test recipe description 2",
        },
    ]

ingredients_to_recipes = [
    {"recipe_id": 1, "ingredient_id": 1, "quantity": "ingr 1 in test recipe 1"},
    {"recipe_id": 1, "ingredient_id": 2, "quantity": "ingr 2 in test recipe 1"},
    {"recipe_id": 1, "ingredient_id": 3, "quantity": "ingr 3 in test recipe 1"},
    {"recipe_id": 2, "ingredient_id": 1, "quantity": "ingr 1 in test recipe 2"},
    {"recipe_id": 2, "ingredient_id": 3, "quantity": "ingr 3 in test recipe 2"}
    ]
# Создание тестовой БД
# подключение к тестовой БД и использование метаданных для
# создания таблицы при начале тестирования
# В конце тестирования удаляем таблицу

@pytest.fixture(autouse=True, scope='session')
async def setup_database():
    print("fix_1 - async_db_connection start")
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        await conn.execute(insert(Ingredient), ingredients)
        await conn.execute(insert(Recipe), recipes)
        await conn.execute(insert(IngredientsInRecipe), ingredients_to_recipes)
        
        await conn.commit()

    yield test_engine

    async with test_engine.begin() as conn:
        print("fix_1 - async_db_connection finish")
        await conn.run_sync(Base.metadata.drop_all)


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
    async with AsyncClient(transport=ASGITransport(app=main_app), base_url="http://test") as async_client:
        yield async_client  # отдаем асинх клиента, чтобы он мог сделать запрос. Вызов из контекстного менеджера гарантирует закрытие после сессии (сессия - прогон всех тестов)

