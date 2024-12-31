# схема для отображения полей класса recipe
from typing import List

from pydantic import BaseModel, ConfigDict


class RecipeBase(BaseModel):
    recipe_name: str = "Омлет с молоком"
    recipe_description: str = (
        "Взбить яйца с молоком в вылить на горячую сковороду. Закрыть крышкой."
    )
    cooking_time: int = 15
    count_views: int = 5


class IngredientsInRecipe(BaseModel):
    ingredient_id: int
    quantity: str = "Количество продукта в рецепте"


class RecipeCreate(RecipeBase):
    ingredients: List[IngredientsInRecipe]


class RecipeRead(RecipeBase):
    model_config = ConfigDict(
        from_attributes=True,
    )
    id: int


class Ingredient(BaseModel):
    name: str
    description: str
    quantity: str


class RecipeDetail(BaseModel):
    id: int
    recipe_name: str
    cooking_time: int
    count_views: int
    recipe_description: str
    ingredients: List[Ingredient]
