import pytz
from fastapi import APIRouter

from app.schemas.reservation import ReservationCreate, Reservation
from app.services.reservation_dao import ReservationDAO

router = APIRouter()


@router.get("/reservations/")
async def get_reservations() -> list[Reservation]:
    reservations = await ReservationDAO.get_reservation()

    # Установка часового пояса
    local_tz = pytz.timezone('Europe/Moscow')

    # Конвертируем временные метки в нужный часовой пояс
    for reservation in reservations:
        if reservation.reservation_time.tzinfo is None:
            reservation.reservation_time = reservation.reservation_time.replace(tzinfo=pytz.utc)
        reservation.reservation_time = reservation.reservation_time.astimezone(local_tz)
    return reservations


@router.post("/reservations/", )
async def create_reservation(reservation: ReservationCreate):
    return await ReservationDAO.create_reservation(reservation.customer_name, reservation.table_id,
                                                   reservation.reservation_time, reservation.duration_minutes)


@router.delete("/reservations/{reservation_id}", )
async def delete_reservation(reservation_id: int):
    return await ReservationDAO.delete(id=reservation_id)
