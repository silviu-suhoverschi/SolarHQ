from __future__ import annotations
from ..models import MonthlyEnergyRecord, ProsumerPricing
from ..schemas.services import ExportIncomeResult, MonthlyExportIncome


def _get_export_price_for_month(year: int, month: int, prosumer_prices: list[ProsumerPricing]) -> float:
    for p in prosumer_prices:
        if p.year == year and p.month == month:
            return p.export_price
    relevant = [p for p in prosumer_prices if (p.year < year) or (p.year == year and p.month < month)]
    if relevant:
        return sorted(relevant, key=lambda x: (x.year, x.month), reverse=True)[0].export_price
    return 0.25


async def calc_export_income(
    energy_records: list[MonthlyEnergyRecord],
    prosumer_prices: list[ProsumerPricing],
) -> ExportIncomeResult:
    if not energy_records:
        return ExportIncomeResult(total_export_income=0.0, monthly_export_income=[], currency="RON")

    total_income = 0.0
    monthly = []

    for record in energy_records:
        price = _get_export_price_for_month(record.year, record.month, prosumer_prices)
        income = record.grid_export * price
        monthly.append(MonthlyExportIncome(year=record.year, month=record.month, value=round(income, 2)))
        total_income += income

    return ExportIncomeResult(
        total_export_income=round(total_income, 2),
        monthly_export_income=monthly,
        currency="RON",
    )
