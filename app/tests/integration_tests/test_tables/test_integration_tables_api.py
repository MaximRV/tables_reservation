import pytest
from httpx import AsyncClient


@pytest.mark.parametrize(
    "name, seats, location, status_code",
    [
        ("Стол-1", 2, "Центральный", 200),
        ("Стол-2", 4, "Левое крыло", 200),
        ("Стол-3", 6, "Правое крыло", 200),
        ("Стол-4", 8, 12, 422),
        (1, 8, "Мансарда", 422),
        ("Стол-6", {"seats": 12}, "Мансарда", 422),
    ],
)
async def test_create_(name, seats, location, status_code, ac: AsyncClient):
    response = await ac.post(
        "/api/v1/tables/",
        json={
            "name": name,
            "seats": seats,
            "location": location
        },
    )
    assert response.status_code == status_code
