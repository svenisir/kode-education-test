from sqlalchemy import ChunkedIteratorResult, insert, select
from sqlalchemy.orm import DeclarativeBase

from app.database import async_session_maker


class BaseDAO:
    model: DeclarativeBase = None

    @classmethod
    async def add(cls, **data):
        async with async_session_maker() as session:
            query = insert(cls.model).values(**data)
            await session.execute(query)
            await session.commit()

    @classmethod
    async def find_by_id(cls, item_id: int):
        async with async_session_maker() as session:
            query = select(cls.model.__table__.columns).filter_by(id=item_id)
            result: ChunkedIteratorResult = await session.execute(query)
            return result.mappings().one_or_none()
