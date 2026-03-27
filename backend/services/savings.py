from __future__ import annotations
from ..models import MonthlyEnergyRecord, GridPrice, SavingOffset
from ..schemas.services import SavingsResult, MonthlySaving


def _get_price_for_month(year: int, month: int, grid_prices: list[GridPrice]) -> float:
    for p in grid_prices:
        if p.year == year and p.month == month:
            return p.price_per_kwh
    relevant = [p for p in grid_prices if (p.year < year) or (p.year == year and p.month < month)]
    if relevant:
        return sorted(relevant, key=lambda x: (x.year, x.month), reverse=True)[0].price_per_kwh
    return 0.8


async def calc_savings(
    energy_records: list[MonthlyEnergyRecord],
    grid_prices: list[GridPrice],
    offset: SavingOffset | None,
) -> SavingsResult:
    if not energy_records:
        currency = offset.currency if offset else "RON"
        return SavingsResult(total=offset.value if offset else 0.0, monthly=[], currency=currency)

    currency = offset.currency if offset else "RON"
    offset_value = offset.value if offset else 0.0
    monthly = []
    total_saved = 0.0

    for record in energy_records:
        price = _get_price_for_month(record.year, record.month, grid_prices)
        avoided = max(0.0, (record.load - record.grid_import)) * price
        monthly.append(MonthlySaving(
            year=record.year,
            month=record.month,
            value=round(avoided, 2),
            currency=currency,
        ))
        total_saved += avoided

    return SavingsResult(
        total=round(total_saved + offset_value, 2),
        monthly=monthly,
        currency=currency,
    )
