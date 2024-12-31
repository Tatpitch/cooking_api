# файл test_router.py

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_root(async_client: AsyncClient):
    # тест проверки главной страницы
    response = await async_client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Main page cooking book"}


@pytest.mark.asyncio
async def test_get_all_ingredients(async_client: AsyncClient):
    """
    Асинхронный тест для чтения всех инградиентов из тестовой БД - GET запрос
    """
    response = await async_client.get("/ingredients")
    assert response.status_code == 200
    assert len(response.json()) == 3


@pytest.mark.asyncio
async def test_get_all_recipes(async_client: AsyncClient):
    """
    Асинхронный тест для чтения всех рецептов из тестовой БД - GET запрос
    """
    response = await async_client.get("/recipes")
    assert response.status_code == 200
    assert len(response.json()) == 2


@pytest.mark.asyncio
async def test_get_recipe_detail(async_client: AsyncClient):
    """
    Асинхронный тест для получения детальной информации о рецепте
    из тестовой БД - GET запрос
    """
    response = await async_client.get("/recipes/1")
    assert response.status_code == 200
    assert len(response.json()[0]["ingredients"]) == 3


@pytest.mark.asyncio
async def test_add_ingredient(async_client: AsyncClient):
    """
    Асинхронный тест для добавления инградиента в тестовую БД - POST запрос
    """
    data_test_add_ingredient = {
        "ingredient_name": "adding ingredient",
        "ingredient_description": "description for adding ingredient",
    }

    response = await async_client.post(
        "/ingredients", json=data_test_add_ingredient
    )

    assert response.status_code == 200
    assert (response.json()["ingredient_name"]) == "adding ingredient"
    assert (
        response.json()["ingredient_description"]
    ) == "description for adding ingredient"


@pytest.mark.asyncio
async def test_add_recipe(async_client: AsyncClient):
    """
    Асинхронный тест для добавления рецепта в тестовую БД - POST запрос
    """
    data_test_add_recipe = {
        "recipe_name": "adding recipe",
        "cooking_time": 25,
        "count_views": 0,
        "description": "description for adding recipe",
        "ingredients": [
            {
                "ingredient_id": 1,
                "quantity": "quantity ingredient  adding recipe",
            }
        ],
    }

    response = await async_client.post("/recipes", json=data_test_add_recipe)

    assert response.status_code == 200
    assert response.json()["recipe_name"] == "adding recipe"
