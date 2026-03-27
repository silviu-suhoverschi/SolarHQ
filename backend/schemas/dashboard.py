from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from .services import (
    SavingsResult, ROIResult, PaybackResult, ProjectionResult,
    SolarPriceResult, SelfConsumptionResult, ExportIncomeResult,
    CapacityResult, TrendsResult,
)


class DashboardResponse(BaseModel):
    savings: SavingsResult
    roi: ROIResult
    payback: PaybackResult
    projection: ProjectionResult
    solar_price: SolarPriceResult
    self_consumption: SelfConsumptionResult
    export_income: ExportIncomeResult
    capacity: CapacityResult
    trends: TrendsResult
    last_sync: Optional[datetime]
    currency: str
