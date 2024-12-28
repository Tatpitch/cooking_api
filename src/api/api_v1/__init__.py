from fastapi import APIRouter
# from core.config import settings

from .recipes import router as recipes_router
from .ingredients import router as ingredients_router
from .main_page import router as main_router

router = APIRouter()

router.include_router(main_router)
router.include_router(recipes_router)
router.include_router(ingredients_router)
