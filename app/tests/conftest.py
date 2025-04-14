import asyncio
import json
from datetime import datetime


import pytest_asyncio
from sqlalchemy import insert
from httpx import AsyncClient


from app.config import settings
from app.database import Base, async_session_maker, engine
from app.models.reservation import Reservation
from app.models.table import Table
from app.main import app as fastapi_app

@pytest_asyncio.fixture(scope="session",autouse=True)
async def prepare_database():
    assert settings.MODE == "TEST"

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    def open_mock_json(model: str):
        with open(f"app/tests/mock_{model}.json", encoding="utf-8") as file:
            return json.load(file)

    tables = open_mock_json("tables")
    reservations = open_mock_json("reservations")

    for reservation in reservations:
        reservation["reservation_time"] = datetime.strptime(
            reservation["reservation_time"],'%Y-%m-%dT%H:%M:%S.%fZ')



    async with async_session_maker() as session:
        add_tables = insert(Table).values(tables)
        add_reservations = insert(Reservation).values(reservations)


        await session.execute(add_tables)
        await session.execute(add_reservations)


        await session.commit()

@pytest_asyncio.fixture(scope="session")
def event_loop(request):
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="function")
async def ac():
    async with AsyncClient(app=fastapi_app,base_url="http://test") as async_client:
        yield async_client