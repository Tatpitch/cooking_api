from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from api import router as api_router
from core.config import settings
from core.models import db_helper

# создание прил
main_app = FastAPI()


# Отдаются и закрываются все сессии для работы с БД
@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    yield
    # shutdown
    await db_helper.dispose()


main_app = FastAPI(lifespan=lifespan)
# все роуты
main_app.include_router(api_router)


if __name__ == "__main__":
    # настройка подключения к серверу
    uvicorn.run(
        "main:main_app",
        host=settings.run.host,
        port=settings.run.port,
        reload=True,
    )
