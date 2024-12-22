# обработка запросов для класса Ingredient
from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Ingredient
from core.schemas.ingredient import IngredientCreate


# получение всех инградиентов
async def get_all_ingredients(
        session: AsyncSession,
) -> Sequence[Ingredient]:
    stmt = select(Ingredient).order_by(Ingredient.id)
    result = await session.scalars(stmt)
    return result.all()


# создание нового инградиента
async def create_ingedient(
        session: AsyncSession,
        ingredient_create: IngredientCreate,
) -> Ingredient:
    ingredient = Ingredient(**ingredient_create.model_dump())
    session.add(ingredient)
    await session.commit()
    return ingredient
