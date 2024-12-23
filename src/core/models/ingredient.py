from typing import TYPE_CHECKING, List
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, int_pk, str_uniq, str_null_true

if TYPE_CHECKING:
    from .recipe import Recipe

class Ingredient(Base):
    """
    класс инградиента, входящего в рецепт блюда
    """
    id: Mapped[int_pk]
    ingredient_name: Mapped[str_uniq]
    ingredient_description: Mapped[str_null_true]
    used_in_recipe: Mapped[List["Recipe"]] = relationship(
        back_populates="used_ingredients", secondary="ingredientsinrecipes"
    )

    def __repr__(self):
        return (
            f"ingredient ID = {self.id}, ingredient name = {self.ingredient_name}"
            f"ingredient description = {self.ingredient_description}"
        )



