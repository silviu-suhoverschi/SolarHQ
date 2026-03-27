from datetime import datetime
from sqlalchemy import UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column
from ..database import Base

class MonthlyEnergyRecord(Base):
    __tablename__ = "monthly_energy"
    id: Mapped[int] = mapped_column(primary_key=True)
    year: Mapped[int]
    month: Mapped[int]
    solar: Mapped[float] = mapped_column(default=0)
    load: Mapped[float] = mapped_column(default=0)
    grid_import: Mapped[float] = mapped_column(default=0)
    grid_export: Mapped[float] = mapped_column(default=0)
    battery_charge: Mapped[float | None] = mapped_column(default=None, nullable=True)
    battery_discharge: Mapped[float | None] = mapped_column(default=None, nullable=True)
    source: Mapped[str] = mapped_column(default="ha_sync") # "manual" or "ha_sync"
    
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())

    __table_args__ = (UniqueConstraint("year", "month", name="uq_monthly_energy_year_month"),)
