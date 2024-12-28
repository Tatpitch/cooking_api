from fastapi import APIRouter
from core.schemas.main_page import MainBase
router = APIRouter()


@router.get("/", tags=["главная страница кулинарной книги"], response_model=MainBase)
def main_page():
    return {'message': "Main page cooking book"}
