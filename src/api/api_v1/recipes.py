# запросы для класса Recipe
from typing import Annotated, List

from fastapi import (
    APIRouter,
    Depends,
)
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper
from core.schemas.recipe import (
    RecipeRead,
    RecipeCreate,
    RecipeDetail,
)
from crud import recipes as recipes_crud

router = APIRouter(tags=["Recipes"])

# получение всех рецептов
@router.get("/recipes",
            summary="Get list all recipes",
            response_model=List[RecipeRead])
async def get_recipes(
    # session: AsyncSession = Depends(db_helper.session_getter),
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
):
    recipes = await recipes_crud.get_all_recipes(session=session)
    return recipes


# получение детальной информации о рецепте по его id
@router.get(
    "/recipes/{recipe_id}",
    summary="Get detail information about recipe",
    response_model=RecipeDetail
)
async def get_recipe_by_id(
    session: Annotated[
    AsyncSession,
    Depends(db_helper.session_getter),
],
recipe_id: int,
):
    recipe = await recipes_crud.get_recipe_by_id(
        session=session, recipe_id=recipe_id
    )
    return recipe


# создание нового рецепта
@router.post("/recipes",
             summary="Create new recipe",
             response_model=RecipeRead)
async def create_recipe(
session: Annotated[
    AsyncSession,
    Depends(db_helper.session_getter),
    ],
    recipe_data: RecipeCreate,
):
    print("Add new recipe", recipe_data)
    print("Before call recipes_crud.create_recipe")
    recipe = await recipes_crud.create_recipe(
        session=session,
        recipe_create=recipe_data,
    )
    print("new recipe", recipe['recipe_name'])
    return recipe
