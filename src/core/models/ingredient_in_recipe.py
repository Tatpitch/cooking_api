from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, int_pk, str_uniq, str_null_true

class IngredientsInRecipe(Base):
    """
    Класс для таблицы, связывающую рецепты и инградиенты (многие ко многим)
    Рецепт - инградиент и его количество
    """
    recipe_id: Mapped[int] = mapped_column(ForeignKey("recipes.id", ondelete="CASCADE"),
                                           primary_key=True)
    ingredient_id: Mapped[int] = mapped_column(ForeignKey("ingredients.id", ondelete="CASCADE"),
                                           primary_key=True)
    quantity: Mapped[float | None]

    def __repr__(self):
        return (f"IngredientsInRecipe (recipe_id = {self.recipe_id}, "
                f"ingredient_id = {self.ingredient_id}, "
                f"quantity = {self.quantity}")
