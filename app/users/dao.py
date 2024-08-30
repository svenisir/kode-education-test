from pydantic import EmailStr
from sqlalchemy import ChunkedIteratorResult, select

from app.dao.base import BaseDAO
from app.database import async_session_maker
from app.users.models import Users


class UserDAO(BaseDAO):
    model = Users

    @classmethod
    async def get_one_or_none(cls, email: EmailStr):
        async with async_session_maker() as session:
            query = select(cls.model.__table__.columns).filter_by(email=email)
            result: ChunkedIteratorResult = await session.execute(query)
            return result.mappings().one_or_none()
