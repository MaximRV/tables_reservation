from fastapi import APIRouter

from app.logger import logger
from app.schemas.table import TableCreate,TableBase
from app.services.table_dao import TableDAO

router = APIRouter()


@router.get("/tables/", response_model=list[TableBase])
async def get_tables():
    return await TableDAO.find_all()


@router.post("/tables/")
async def create_table(table: TableCreate):
    logger.info(f"Создание таблицы с именем: {table.name}, местами: {table.seats}, локацией: {table.location}")
    await TableDAO.add(name=table.name, seats=table.seats, location=table.location)
    logger.info("Таблица успешно создана")


@router.delete("/tables/{table_id}")
async def delete_table(table_id: int):
    await TableDAO.delete(id=table_id)
    return table_id
