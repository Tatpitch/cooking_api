from datetime import datetime
from typing import Annotated
from sqlalchemy import func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.orm import declared_attr

from core.config import settings

# настройка аннотаций
int_pk = Annotated[int, mapped_column(primary_key=True)]
create_at = Annotated[datetime, mapped_column(server_default=func.now())]
update_at = Annotated[datetime, mapped_column(server_default=func.now(),
                                              onupdate=datetime.now)]
str_uniq = Annotated[str, mapped_column(unique=True, nullable=False)]
str_null_true = Annotated[str, mapped_column(nullable=True)]

class Base(DeclarativeBase):
    """
    базовый класс для всех моделей таблиц
    """
    __abstract__ = True
    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f"{(cls.__name__.lower())}s"
    create_at: Mapped[create_at]
    update_at: Mapped[update_at]
