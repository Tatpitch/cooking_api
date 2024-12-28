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
    # id: Mapped[int_pk]
    ingredient_name: Mapped[str_uniq]
    ingredient_description: Mapped[str_null_true]
    used_in_recipe: Mapped[List["IngredientsInRecipe"]] = relationship(
        back_populates="ingredient")
    # used_in_recipe: Mapped[List["Recipe"]] = relationship(
    #     back_populates="used_ingredients", secondary="ingredientsinrecipes"
    # )

    def __repr__(self):
        return (
            f"ingredient ID = {self.id}, ingredient name = {self.ingredient_name}"
            f"ingredient description = {self.ingredient_description}"
        )
