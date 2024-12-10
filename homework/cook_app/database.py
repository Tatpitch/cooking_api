from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import DeclarativeBase
# from sqlalchemy.ext.declarative import declarative_base
from typing import AsyncGenerator
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite+aiosqlite:///./cookbook.db"

engine = create_async_engine(DATABASE_URL, echo=True)
# expire_on_commit=False will prevent attributes from being expired
# after commit.
# async_session = sessionmaker(
#     engine, expire_on_commit=False, class_=AsyncSession
# )
# session = async_session()

async_session_global = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_global() as session:
        try:
            yield session
        except:
            await session.rollback()
            raise
        finally:
            await session.close()

class Base(DeclarativeBase):
    pass

