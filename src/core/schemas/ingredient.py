# схема для отображения полей класса ingredient
from pydantic import BaseModel
from pydantic import ConfigDict


class IngredientBase(BaseModel):
    ingredient_name: str = "Молоко (наименование)"
    ingredient_description: str = "Молоко коровье пастеризованное (описание)"


class IngredientCreate(IngredientBase):
    pass


class IngredientRead(IngredientBase):
    model_config = ConfigDict(
        from_attributes=True,
    )

    id: int