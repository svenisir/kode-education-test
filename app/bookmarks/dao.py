from sqlalchemy import ChunkedIteratorResult, select
from sqlalchemy.orm import DeclarativeBase, joinedload

from app.bookmarks.models import Bookmarks
from app.dao.base import BaseDAO
from app.database import async_session_maker


class BookmarksDAO(BaseDAO):
    model: DeclarativeBase = Bookmarks

    @classmethod
    async def get_all_bookmarks(cls, user_id):
        async with async_session_maker() as session:
            query = (
                select(cls.model.__table__.columns)
                .options(joinedload(cls.model.user))
                .filter_by(user_id=user_id)
            )

            result: ChunkedIteratorResult = await session.execute(query)
            return result.mappings().all()
