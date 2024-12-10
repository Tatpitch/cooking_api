from pydantic import BaseModel, Field


class BaseRecipe(BaseModel):
    title: str = Field(min_length=3, max_length=50)
    cooking_time: int = Field(g=0, le=300)
    count_views: int



class RecipeIn(BaseRecipe):
    list_ingredients: str
    description: str

class RecipeOut(BaseRecipe):
    ...

    class Config:
        orm_mode = True


class FullRecipeOut(BaseRecipe):
    id: int
    list_ingredients: str
    description: str


    class Config:
        orm_mode = True

