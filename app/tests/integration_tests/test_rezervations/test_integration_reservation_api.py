import pytest
from httpx import AsyncClient


@pytest.mark.parametrize(
    "customer_name, table_id, reservation_time, duration_minutes, status_code",
    [
        ("Andrey", 1, "2025-04-14T19:17:09.374Z", 5, 200),
        ("Maxim", 2, "2025-04-14T19:17:09.374Z", 10, 200),
        ("Alex", 3, "2025-04-14T19:17:09.374Z", 15, 200),
        ("Nicolai", 4, "2025-04-14T19:21:09.374Z", 20, 500),
        ("Nicol", 3, "2025-04-14T19:25:09.374Z", 60, 400),
        (1, 8, "2025-04-14T19:17:09.374Z", 60, 422),
        ("Виталий", {"seats": 12}, "Мансарда", 20, 422),

    ],
)

async def test_create_reservation(customer_name, table_id, reservation_time, duration_minutes, status_code,
                                  ac: AsyncClient):
    response = await ac.post(
        "/api/v1/reservations/",
        json={
            "customer_name": customer_name,
            "table_id": table_id,
            "reservation_time": reservation_time,
            "duration_minutes": duration_minutes,
        },
    )
    assert response.status_code == status_code
