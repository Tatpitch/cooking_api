from pygments.lexer import default
from sqlalchemy import Column, String, Integer


from database import Base


class Recipe(Base):
    __tablename__ = 'Cookbook'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    cooking_time = Column(Integer, index=True)
    count_views = Column(Integer, index=True, default=0)
    list_ingredients = Column(String)
    description = Column(String)
