import calendar
from ..models import MonthlyEnergyRecord
from ..schemas.services import CapacityResult


async def calc_capacity(
    energy_records: list[MonthlyEnergyRecord],
    panel_capacity_kw: float = 0.0,
) -> CapacityResult:
    if not energy_records:
        return CapacityResult(estimated_kwp=0.0, avg_capacity_factor=None, avg_peak_sun_hours=None)

    capacity_factors = []
    peak_sun_hours_list = []

    for r in energy_records:
        days = calendar.monthrange(r.year, r.month)[1]
        hours = days * 24
        if panel_capacity_kw > 0 and r.solar > 0:
            capacity_factors.append(r.solar / (panel_capacity_kw * hours))
            peak_sun_hours_list.append(r.solar / (panel_capacity_kw * days))

    avg_cf = round(sum(capacity_factors) / len(capacity_factors), 4) if capacity_factors else None
    avg_psh = round(sum(peak_sun_hours_list) / len(peak_sun_hours_list), 2) if peak_sun_hours_list else None

    if panel_capacity_kw > 0:
        estimated_kwp = panel_capacity_kw
    else:
        # Estimate from production: European avg ~1100 kWh/kWp/year
        months = len(energy_records)
        annual_solar = (sum(r.solar for r in energy_records) / months) * 12 if months else 0
        estimated_kwp = round(annual_solar / 1100, 2)

    return CapacityResult(
        estimated_kwp=estimated_kwp,
        avg_capacity_factor=avg_cf,
        avg_peak_sun_hours=avg_psh,
    )
