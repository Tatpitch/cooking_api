from typing import TYPE_CHECKING, List
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, int_pk, str_uniq, str_null_true
from .mixins.int_id_pk import IntIdPkMixin

if TYPE_CHECKING:
    from .recipe import Recipe
    from .ingredient_in_recipe import IngredientsInRecipe

class Ingredient(IntIdPkMixin, Base):
    """
    класс инградиента, входящего в рецепт блюда
    """
    ingredient_name: Mapped[str_uniq]
    ingredient_description: Mapped[str_null_true]
    used_in_recipe: Mapped[List["IngredientsInRecipe"]] = relationship(
        back_populates="ingredient")


    def __repr__(self):
        return (
            f"ingredient ID = {self.id}, ingredient name = {self.ingredient_name}"
            f"ingredient description = {self.ingredient_description}"
        )
