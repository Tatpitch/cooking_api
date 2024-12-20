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
)
from crud import recipes as recipes_crud

router = APIRouter(tags=["Recipes"])
