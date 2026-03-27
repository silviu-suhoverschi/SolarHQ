from ..models import MonthlyEnergyRecord
from ..schemas.services import SelfConsumptionResult


async def calc_self_consumption(
    energy_records: list[MonthlyEnergyRecord],
) -> SelfConsumptionResult:
    if not energy_records:
        return SelfConsumptionResult(
            self_consumed_kwh=0.0,
            self_consumption_percent=0.0,
            autarky_percent=0.0,
        )

    total_produced = sum(r.solar for r in energy_records)
    total_load = sum(r.load for r in energy_records)
    self_consumed_kwh = sum(max(0.0, r.load - r.grid_import) for r in energy_records)

    self_consumption_pct = (self_consumed_kwh / total_produced * 100) if total_produced > 0 else 0.0
    autarky_pct = (self_consumed_kwh / total_load * 100) if total_load > 0 else 0.0

    return SelfConsumptionResult(
        self_consumed_kwh=round(self_consumed_kwh, 2),
        self_consumption_percent=round(self_consumption_pct, 1),
        autarky_percent=round(autarky_pct, 1),
    )
