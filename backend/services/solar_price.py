from ..models import MonthlyEnergyRecord, Cost
from ..schemas.services import SolarPriceResult


async def calc_solar_price(
    energy_records: list[MonthlyEnergyRecord],
    costs: list[Cost],
) -> SolarPriceResult:
    total_produced = sum(r.solar for r in energy_records)
    total_investment = sum(c.value for c in costs)

    if total_produced == 0:
        return SolarPriceResult(cost_per_kwh_produced=0.0, total_produced=0.0, currency="RON")

    cost_per_kwh = total_investment / total_produced

    return SolarPriceResult(
        cost_per_kwh_produced=round(cost_per_kwh, 4),
        total_produced=round(total_produced, 2),
        currency="RON",
    )
