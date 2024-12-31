# обработка запросов для класса Recipe
from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Ingredient, IngredientsInRecipe, Recipe
from core.schemas.recipe import RecipeCreate


# получение всех рецептов
async def get_all_recipes(
    session: AsyncSession,
) -> Sequence[Recipe]:
    stmt = select(Recipe).order_by(Recipe.id)
    result = await session.scalars(stmt)
    return result.all()


# получение детальной информации о рецепте по его id
async def get_recipe_by_id(session: AsyncSession, recipe_id: int):
    # информация о рецепте из таблицы recipes
    print("recipe_id = ", recipe_id)
    result = await session.execute(
        select(Recipe).filter(Recipe.id == recipe_id)
    )
    print("result by id ", result)
    # информация об инградиентах найденного рецепта
    result_ingredients = await session.execute(
        select(
            IngredientsInRecipe.quantity,
            Ingredient.ingredient_name,
            Ingredient.ingredient_description,
        )
        .join(Ingredient, Ingredient.id == IngredientsInRecipe.ingredient_id)
        .where(IngredientsInRecipe.recipe_id == recipe_id)
    )
    recipe = result.scalars().one()
    # ingredients = result_ingredients.fetchall()
    ingredients = result_ingredients.fetchall()
    recipe.count_views += 1
    print("count_views", recipe.count_views)
    await session.commit()

    recipe_with_ingredients = [
        {
            "id": recipe.id,
            "recipe_name": recipe.recipe_name,
            "cooking_time": recipe.cooking_time,
            "recipe_description": recipe.recipe_description,
            "count_views": recipe.count_views,
            "ingredients": [
                {
                    "name": i.ingredient_name,
                    "description": i.ingredient_description,
                    "quantity": i.quantity,
                }
                for i in ingredients
            ],
        },
    ]
    return recipe_with_ingredients


# создание нового рецепта
async def create_recipe(
    session: AsyncSession,
    recipe_create: RecipeCreate,
) -> Recipe:
    print("crud/ recipe")
    data = recipe_create.model_dump()
    print(data["recipe_name"])
    print(data["ingredients"])
    recipe = Recipe(
        recipe_name=data["recipe_name"],
        recipe_description=data["recipe_description"],
        cooking_time=data["cooking_time"],
        count_views=data["count_views"],
    )
    session.add(recipe)
    await session.flush()
    print("new recipe", recipe)
    ingredients_in_recipe = []
    print("new recipe_id", recipe.id)

    for item in data["ingredients"]:
        ingredients_in_recipe.append(
            IngredientsInRecipe(
                recipe_id=recipe.id,
                ingredient_id=item["ingredient_id"],
                quantity=item["quantity"],
            )
        )
    print("ingredients in recipe", ingredients_in_recipe)
    session.add_all(ingredients_in_recipe)
    await session.commit()
    # await session.refresh(recipe)
    return recipe
