from typing import TYPE_CHECKING, List
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, int_pk, str_uniq, str_null_true

if TYPE_CHECKING:
    from .ingredient import Ingredient

class Recipe(Base):
    """
    класс рецепта
    """
    id: Mapped[int_pk]
    recipe_name: Mapped[str_uniq]
    cooking_time: Mapped[int] = mapped_column(default=10)
    count_views: Mapped[int] = mapped_column(default=0)
    recipe_description: Mapped[str_null_true]

    used_ingredients: Mapped[List["Ingredient"]] = relationship(
        back_populates="used_in_recipe", secondary="ingredientsinrecipes"
    )

    def __repr__(self):
        return f"Recipe: ID = {self.id}, title = {self.recipe_name}"
