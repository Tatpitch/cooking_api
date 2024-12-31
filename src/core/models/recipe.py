from typing import TYPE_CHECKING, List

from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, str_null_true, str_uniq
from .mixins.int_id_pk import IntIdPkMixin

if TYPE_CHECKING:
    from .ingredient_in_recipe import IngredientsInRecipe


class Recipe(IntIdPkMixin, Base):
    """
    класс рецепта
    """

    recipe_name: Mapped[str_uniq]
    cooking_time: Mapped[int] = mapped_column(default=10)
    count_views: Mapped[int] = mapped_column(default=0)
    recipe_description: Mapped[str_null_true]
    used_ingredients: Mapped[List["IngredientsInRecipe"]] = relationship(
        back_populates="recipe"
    )

    def __repr__(self):
        return f"Recipe: ID = {self.id}, title = {self.recipe_name}"
