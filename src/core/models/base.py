from datetime import datetime
from typing import Annotated

from sqlalchemy import MetaData, func
from sqlalchemy.orm import DeclarativeBase, declared_attr, mapped_column

from core.config import settings

# настройка аннотаций
int_pk = Annotated[int, mapped_column(primary_key=True)]
create_at = Annotated[datetime, mapped_column(server_default=func.now())]
update_at = Annotated[
    datetime, mapped_column(server_default=func.now(), onupdate=datetime.now)
]
str_uniq = Annotated[str, mapped_column(unique=True, nullable=False)]
str_null_true = Annotated[str, mapped_column(nullable=True)]


class Base(DeclarativeBase):
    """
    базовый класс для всех моделей таблиц
    """

    __abstract__ = True

    metadata = MetaData(
        naming_convention=settings.db.naming_convention,
    )

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f"{(cls.__name__.lower())}s"
