from fastapi import APIRouter
from core.config import settings

from .recipes import router as recipes_router
from .ingredients import router as ingredients_router
from .main_page import router as main_router

router = APIRouter(
    prefix=settings.api.v1.prefix,
)
router.include_router(
    main_router,
    recipes_router,
    ingredients_router,
    prefix=settings.api.v1.users,
)