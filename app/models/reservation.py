from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Integer, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from app.models.table import Table


class Reservation(Base):
    __tablename__ = "reservations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    customer_name: Mapped[str]
    table_id: Mapped[int] = mapped_column(ForeignKey("tables.id"))
    reservation_time: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    duration_minutes: Mapped[int]

    table: Mapped["Table"] = relationship(back_populates="reservations")

    def __str__(self):
        return f"Резервация {self.id}"
