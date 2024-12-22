from fastapi import APIRouter
# from core.config import settings
from .api_v1 import router as router_api_v1

# основной роутер приложения

router = APIRouter()
router.include_router(router_api_v1)
