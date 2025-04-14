from sqlalchemy import delete, insert, select

from app.database import async_session_maker
from app.logger import logger


class BaseDAO:
    model = None

    @classmethod
    async def find_all(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model.__table__.columns).filter_by(**filter_by)
            result = await session.execute(query)
            return result.mappings().all()

    @classmethod
    async def add(cls, **data: dict):
        async with async_session_maker() as session:
            try:
                logger.info(f"Adding data: {data}")
                query = insert(cls.model).values(**data).returning(cls.model)
                result = await session.execute(query)
                await session.commit()
                return result.scalar()  # Возвращает добавленный объект
            except Exception as e:
                await session.rollback()
                logger.error(f"Error adding data: {e}")
                raise

    @classmethod
    async def delete(cls, **filter_by):
        async with async_session_maker() as session:
            try:
                query = delete(cls.model).filter_by(**filter_by)
                result = await session.execute(query)
                await session.commit()
                return result.rowcount
            except Exception as e:
                await session.rollback()
                raise e
