from http.client import HTTPException
from typing import List

import sqlalchemy.orm
from fastapi import FastAPI, Path
from fastapi.params import Depends

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from tornado.httpclient import HTTPError

import models
import schemas
from database import engine, get_async_session

app = FastAPI()


@app.on_event("startup")
async def shutdown():
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)


@app.on_event("shutdown")
async def shutdown(session: AsyncSession = Depends(get_async_session)):
    await session.close()
    await engine.dispose()


@app.get('/')
async def get_hello():
    return 'Hello'


@app.get('/recipes/', response_model=List[schemas.RecipeOut])
async def get_all_recipes(session: AsyncSession = Depends(get_async_session)) -> List[models.Recipe]:
    res = await session.execute(select(models.Recipe))
    return res.scalars().all()


@app.get('/recipes/{recipe_id}', response_model=schemas.FullRecipeOut)
async def get_recipe(recipe_id: int = Path(..., title='ID of recepi'), session: AsyncSession = Depends(get_async_session)) -> models.Recipe | str:
    res = await session.execute(select(models.Recipe).where(models.Recipe.id == recipe_id))
    dish = res.scalar()
    if dish:
        dish.count_views += 1
        await session.commit()
        return dish
    else:
        raise HTTPException(status_code=400, details='Recipe not found')


@app.post('/recipes/', response_model=schemas.RecipeOut)
async def add_recipe(recipe: schemas.RecipeIn, session: AsyncSession = Depends(get_async_session)) -> models.Recipe | str:
    new_recipe = models.Recipe(**recipe.dict())
    async with session.begin():
        try:
            session.add(new_recipe)
            # session.commit()
            # session.close()
            return new_recipe
        except sqlalchemy.exc.DatabaseError as err:
            session.rollback()
            return f"error {err}"
