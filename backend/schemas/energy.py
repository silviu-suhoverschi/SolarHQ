from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime

class EnergyRecordBase(BaseModel):
    year: int = Field(..., ge=2000, le=2100)
    month: int = Field(..., ge=1, le=12)
    solar: float = 0.0
    load: float = 0.0
    grid_import: float = 0.0
    grid_export: float = 0.0
    battery_charge: float | None = None
    battery_discharge: float | None = None
    source: str = "manual"

class EnergyRecordCreate(EnergyRecordBase):
    pass

class EnergyRecordUpdate(BaseModel):
    solar: float | None = None
    load: float | None = None
    grid_import: float | None = None
    grid_export: float | None = None
    battery_charge: float | None = None
    battery_discharge: float | None = None
    source: str | None = None

class EnergyRecordResponse(EnergyRecordBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
