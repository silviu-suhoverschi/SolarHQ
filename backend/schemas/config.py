from __future__ import annotations
from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime

class AppConfigBase(BaseModel):
    language: str = "en"
    currency: str = "RON"
    sync_enabled: bool = True
    
    # Sensor entity IDs
    sensor_solar: str | None = None
    sensor_load: str | None = None
    sensor_grid_import: str | None = None
    sensor_grid_export: str | None = None
    sensor_battery_charge: str | None = None
    sensor_battery_discharge: str | None = None

class AppConfigUpdate(AppConfigBase):
    pass

class AppConfigResponse(AppConfigBase):
    last_sync: datetime | None = None
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)
