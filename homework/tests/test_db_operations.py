from aiohttp.test_utils import TestClient
from celery.bin.control import status
from httpx import AsyncClient
from main import app
from fastapi.testclient import TestClient
from requests import Response
from sqlalchemy.ext.asyncio import AsyncSession

# from python_advanced.module_13_db2.homework.hw5.main import start_name

client: TestClient = TestClient(app)


# Сами тесты:

async def test_hello(async_client: AsyncClient):
    """
    Ассинхронный тест эендпойнта "/"
    """
    response = await async_client.get("/")
    assert response.status_code == 200
    assert response.json() == "Hello"


def test_hello_syn():
    """
        Cинхронный тест эендпойнта "/"
        """
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == "Hello"


async def test_add_recipe(async_client: AsyncClient):
    """
    Асинхронный тест для добавления рецепта в тестовую БД - POST запрос
    """
    data_test = {
        "title": "Омлет",
        "cooking_time": 20,
        "count_views": 0,
        "list_ingredients": "Яйца, молоко, масло",
        "description": "Взить яйца с молоком и поджарить под крышкой",
         }

    response = await async_client.post('/recipes/', json=data_test)

    assert response.status_code == 200



async def test_get_recipe(async_client: AsyncClient):
    """
        Асинхронный тест для чтения рецепта из тестовой БД - GET запрос
        """
    response = await async_client.get("/recipes/")

    assert response.status_code == 200
    assert "title" in response.json()[0]
    assert response.json()[0]['title'] == "Омлет"
    assert len(response.json()) == 1
