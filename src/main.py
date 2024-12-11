from fastapi import FastAPI
import uvicorn

# создание прил
main_app = FastAPI()


if __name__ == "__main__":
    # настройка подключения к серверу
    uvicorn.run(
        "main:main_app",
                reload=True,
    )
