import asyncio
import json

import pytest
from httpx import AsyncClient
from sqlalchemy import insert

from app.bookmarks.models import Bookmarks
from app.config import settings
from app.database import Base, async_session_maker, engine
from app.main import app as fastapi_app
from app.users.models import Users


@pytest.fixture(scope="session", autouse=True)
async def prepare_database():
    assert settings.MODE == "TEST"

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    def open_mock_json(model: str):
        with open(f"app/tests/mock_{model}.json", "r", encoding="utf-8") as file:
            return json.load(file)

    users = open_mock_json("users")
    bookmarks = open_mock_json("bookmarks")

    async with async_session_maker() as session:
        add_users = insert(Users).values(users)
        add_bookmarks = insert(Bookmarks).values(bookmarks)

        await session.execute(add_users)
        await session.execute(add_bookmarks)

        await session.commit()


@pytest.fixture(scope="session")
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function")
async def ac():
    async with AsyncClient(app=fastapi_app, base_url="http://test") as ac:
        yield ac


@pytest.fixture(scope="session")
async def authenticated_ac():
    async with AsyncClient(app=fastapi_app, base_url="http://test") as ac:
        await ac.post("/auth/login", json={
            "email": "test@test.com",
            "password": "test"
        })
        assert ac.cookies["booking_access_token"]
        yield ac
