from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from typing import Literal

# Saving Offset Singleton
class SavingOffsetBase(BaseModel):
    value: float = 0.0
    currency: str = "RON"

class SavingOffsetResponse(SavingOffsetBase):
    id: int
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)

# Grid Pricing
class GridPriceBase(BaseModel):
    year: int = Field(..., ge=2000, le=2100)
    month: int = Field(..., ge=1, le=12)
    price_per_kwh: float = Field(..., ge=0)
    time_of_use: Literal["flat", "peak", "offpeak"] = "flat"
    currency: str = "RON"

class GridPriceCreate(GridPriceBase):
    pass

class GridPriceResponse(GridPriceBase):
    id: int
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)

# Prosumer Pricing
class ProsumerPricingBase(BaseModel):
    year: int = Field(..., ge=2000, le=2100)
    month: int = Field(..., ge=1, le=12)
    import_price: float = Field(..., ge=0)
    export_price: float = Field(..., ge=0)
    fixed_tariff: float = 0.0
    tax: float = 0.0
    currency: str = "RON"

class ProsumerPricingCreate(ProsumerPricingBase):
    pass

class ProsumerPricingResponse(ProsumerPricingBase):
    id: int
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)
