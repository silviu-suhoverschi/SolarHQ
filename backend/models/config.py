from __future__ import annotations
from datetime import datetime
from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column
from ..database import Base

class AppConfig(Base):
    """Singleton configuration — HA sensors + global settings"""
    __tablename__ = "app_config"
    id: Mapped[int] = mapped_column(primary_key=True, default=1)
    location_name: Mapped[str] = mapped_column(default="My Home")
    currency: Mapped[str] = mapped_column(default="RON")
    sensor_solar: Mapped[str | None] = mapped_column(nullable=True)
    sensor_load: Mapped[str | None] = mapped_column(nullable=True)
    sensor_grid_import: Mapped[str | None] = mapped_column(nullable=True)
    sensor_grid_export: Mapped[str | None] = mapped_column(nullable=True)
    sensor_battery_charge: Mapped[str | None] = mapped_column(nullable=True)
    sensor_battery_discharge: Mapped[str | None] = mapped_column(nullable=True)
    language: Mapped[str] = mapped_column(default="ro")
    last_sync: Mapped[datetime | None] = mapped_column(nullable=True)
    sync_enabled: Mapped[bool] = mapped_column(default=True)
    
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())
