from datetime import timedelta, datetime, timezone

from fastapi import HTTPException
from sqlalchemy import select, func, text

from app.database import async_session_maker
from app.models.reservation import Reservation
from app.services.base_dao import BaseDAO


class ReservationDAO(BaseDAO):
    model = Reservation

    @classmethod
    async def create_reservation(cls, customer_name: str, table_id: int, reservation_time: datetime,
                                 duration_minutes: int):
        if reservation_time.tzinfo is None:
            reservation_time = reservation_time.replace(tzinfo=timezone.utc)

        end_time = reservation_time + timedelta(minutes=duration_minutes)
        print(end_time)
        if end_time.tzinfo is None:
            end_time = end_time.replace(tzinfo=timezone.utc)

        async with async_session_maker() as session:

            # Проверка на конфликты броней
            get_conflicting_reservations = select(Reservation).filter(Reservation.table_id == table_id,
                                                                      Reservation.reservation_time < end_time,
                                                                      Reservation.reservation_time + text(
                                                                          "INTERVAL '1 minute' * reservations.duration_minutes") > reservation_time)

            conflicting_reservations = await session.execute(get_conflicting_reservations)

            conflicting_reservations_list = conflicting_reservations.scalars().all()

            if conflicting_reservations_list:
                raise HTTPException(status_code=400, detail="Выбранный стол уже зарезервирован для указанного времени.")

            new_reservation = await ReservationDAO.add(customer_name=customer_name, table_id=table_id,
                                                       reservation_time=reservation_time,
                                                       duration_minutes=duration_minutes)

            return new_reservation

    @classmethod
    async def get_reservation(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalars().all()
