from fastapi import APIRouter

from .ingredients import router as ingredients_router
from .main_page import router as main_router
from .recipes import router as recipes_router

# from core.config import settings


router = APIRouter()

router.include_router(main_router)
router.include_router(recipes_router)
router.include_router(ingredients_router)
