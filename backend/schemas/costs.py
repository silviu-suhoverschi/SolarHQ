from pydantic import BaseModel, ConfigDict, Field
from datetime import date, datetime
from typing import computed_field

class CostBase(BaseModel):
    date: date
    description: str
    value: float = Field(..., gt=0)
    currency: str = "RON"
    operating_life_years: int = Field(25, ge=1, le=100)

class CostCreate(CostBase):
    pass

class CostUpdate(BaseModel):
    date: date | None = None
    description: str | None = None
    value: float | None = None
    currency: str | None = None
    operating_life_years: int | None = None

class CostResponse(CostBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

    @computed_field
    @property
    def total_cost(self) -> float:
        return self.value
