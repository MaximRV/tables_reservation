from typing import TYPE_CHECKING

from sqlalchemy import Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from app.models.reservation import Reservation


class Table(Base):
    __tablename__ = "tables"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str]
    seats: Mapped[int]
    location: Mapped[str]

    reservations: Mapped[list["Reservation"]] = relationship(back_populates="table")

    def __str__(self):
        return f"Стол {self.name}"
