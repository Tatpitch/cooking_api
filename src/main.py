from fastapi import FastAPI
import uvicorn
from api import router as api_router
from core.config import settings

# создание прил
main_app = FastAPI()
# все роуты
main_app.include_router(
    api_router,
    prefix=settings.api.prefix
)


if __name__ == "__main__":
    # настройка подключения к серверу
    uvicorn.run(
        "main:main_app",
        host=settings.run.host,
        port=settings.run.port,
        reload=True,
    )
