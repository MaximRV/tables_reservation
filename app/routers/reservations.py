import pytz
from fastapi import APIRouter, HTTPException, Response

from app.logger import logger
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
            logger.debug(f"Time conversion for reservation {reservation.id} From UTC to {local_tz}")
            reservation.reservation_time = reservation.reservation_time.replace(tzinfo=pytz.utc)
        reservation.reservation_time = reservation.reservation_time.astimezone(local_tz)
    return reservations


@router.post("/reservations/")
async def create_reservation(reservation: ReservationCreate):
    try:
        logger.info(f"Creating a reservation for a client {reservation.customer_name}")
        result = await ReservationDAO.create_reservation(
            reservation.customer_name, reservation.table_id,
            reservation.reservation_time, reservation.duration_minutes
        )
        logger.info("Reservation is successfully created")
        return result
    except Exception as e:
        logger.error(f"Reservation error: {e}")
        raise





@router.delete("/reservations/{reservation_id}", status_code=204)
async def delete_reservation(reservation_id: int):
    logger.info(f"Removal of reservation with ID {reservation_id}")

    result = await ReservationDAO.delete(id=reservation_id)
    if result == 0:
        logger.warning(f"reservation with ID {reservation_id} not found")
        raise HTTPException(status_code=404, detail="Бронирование не найдено")

    logger.info(f"reservation with ID {reservation_id} Deleted")
    return Response(status_code=204)

