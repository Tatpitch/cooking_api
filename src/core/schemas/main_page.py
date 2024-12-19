# схема для main_page
from pydantic import BaseModel


class MainBase(BaseModel):
    message: str = "Main page cooking book"


