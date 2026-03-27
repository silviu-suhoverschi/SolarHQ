from datetime import date, datetime
from sqlalchemy import UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column
from ..database import Base

class Cost(Base):
    __tablename__ = "cost"
    id: Mapped[int] = mapped_column(primary_key=True)
    date: Mapped[date]
    description: Mapped[str]
    value: Mapped[float]
    currency: Mapped[str] = mapped_column(default="RON")
    operating_life_years: Mapped[int] = mapped_column(default=25)
    
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())

class SavingOffset(Base):
    __tablename__ = "saving_offset"
    id: Mapped[int] = mapped_column(primary_key=True, default=1)
    value: Mapped[float] = mapped_column(default=0)
    currency: Mapped[str] = mapped_column(default="RON")
    
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())

class GridPrice(Base):
    __tablename__ = "grid_price"
    id: Mapped[int] = mapped_column(primary_key=True)
    year: Mapped[int]
    month: Mapped[int]
    price_per_kwh: Mapped[float]
    time_of_use: Mapped[str] = mapped_column(default="flat") # "flat", "peak", "offpeak"
    currency: Mapped[str] = mapped_column(default="RON")
    
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())

    __table_args__ = (UniqueConstraint("year", "month", "time_of_use", name="uq_grid_price_period_tou"),)

class ProsumerPricing(Base):
    __tablename__ = "prosumer_pricing"
    id: Mapped[int] = mapped_column(primary_key=True)
    year: Mapped[int]
    month: Mapped[int]
    import_price: Mapped[float]
    export_price: Mapped[float]
    fixed_tariff: Mapped[float] = mapped_column(default=0)
    tax: Mapped[float] = mapped_column(default=0)
    currency: Mapped[str] = mapped_column(default="RON")
    
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())

    __table_args__ = (UniqueConstraint("year", "month", name="uq_prosumer_pricing_year_month"),)
