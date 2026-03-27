from pydantic import BaseModel
from datetime import date
from typing import Optional


class MonthlySaving(BaseModel):
    year: int
    month: int
    value: float
    currency: str


class SavingsResult(BaseModel):
    total: float
    monthly: list[MonthlySaving]
    currency: str


class ROIResult(BaseModel):
    roi_percent: float
    total_investment: float


class PaybackResult(BaseModel):
    months_to_payback: Optional[float]
    estimated_date: Optional[date]
    status: str


class YearProjection(BaseModel):
    year: int
    projected_savings: float


class ProjectionResult(BaseModel):
    projected_savings_5y: float
    projected_savings_10y: float
    yearly: list[YearProjection]


class SolarPriceResult(BaseModel):
    cost_per_kwh_produced: float
    total_produced: float
    currency: str


class SelfConsumptionResult(BaseModel):
    self_consumed_kwh: float
    self_consumption_percent: float
    autarky_percent: float


class MonthlyExportIncome(BaseModel):
    year: int
    month: int
    value: float


class ExportIncomeResult(BaseModel):
    total_export_income: float
    monthly_export_income: list[MonthlyExportIncome]
    currency: str


class CapacityResult(BaseModel):
    estimated_kwp: float
    avg_capacity_factor: Optional[float]
    avg_peak_sun_hours: Optional[float]


class SeasonalAverage(BaseModel):
    month: int
    avg_solar: float


class YoYData(BaseModel):
    year: int
    total_solar: float
    total_savings: float


class ROIScenario(BaseModel):
    year: int
    base: float
    optimistic: float
    pessimistic: float


class ROIForecast(BaseModel):
    scenarios: list[ROIScenario]


class TrendsResult(BaseModel):
    seasonal_averages: list[SeasonalAverage]
    year_over_year: list[YoYData]
    roi_forecast: ROIForecast
    yoy_solar_percent: float
    mom_solar_percent: float
    data_points: int
