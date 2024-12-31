# запросы для класса Ingredient
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper
from core.schemas.ingredient import IngredientCreate, IngredientRead
from crud import ingredients as ingredients_crud

# роутер для запросов класса Ingredients
router = APIRouter(tags=["Ingredients"])


# получение всех инградиентов
@router.get(
    "/ingredients",
    summary="Get all ingredients",
    response_model=list[IngredientRead],
)
async def get_ingredients(
    # session: AsyncSession = Depends(db_helper.session_getter),
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
):
    ingredients = await ingredients_crud.get_all_ingredients(session=session)
    return ingredients


# post запрос на создание нового инградиента
@router.post(
    "/ingredients", summary="Add new ingredient", response_model=IngredientRead
)
async def create_ingredient(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
    ingredient_create: IngredientCreate,
):
    ingredient = await ingredients_crud.create_ingedient(
        session=session,
        ingredient_create=ingredient_create,
    )
    return ingredient
