from typing import Annotated

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


@router.get("", response_model=list[RecipeRead])
async def get_recipes(
    # session: AsyncSession = Depends(db_helper.session_getter),
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
):
    recipes = await recipes_crud.get_all_recipes(session=session)
    return recipes

