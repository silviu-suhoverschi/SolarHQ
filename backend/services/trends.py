from __future__ import annotations
from ..models import MonthlyEnergyRecord
from ..schemas.services import (
    TrendsResult, SeasonalAverage, YoYData, ROIForecast, ROIScenario, MonthlySaving,
)


async def calc_trends(
    energy_records: list[MonthlyEnergyRecord],
    savings_by_month: list[MonthlySaving] | None = None,
) -> TrendsResult:
    empty_seasonal = [SeasonalAverage(month=m, avg_solar=0.0) for m in range(1, 13)]

    if not energy_records:
        return TrendsResult(
            seasonal_averages=empty_seasonal,
            year_over_year=[],
            roi_forecast=ROIForecast(scenarios=[]),
            yoy_solar_percent=0.0,
            mom_solar_percent=0.0,
            data_points=0,
        )

    # Seasonal averages for all 12 months
    seasonal: dict[int, list[float]] = {m: [] for m in range(1, 13)}
    for r in energy_records:
        seasonal[r.month].append(r.solar)
    seasonal_averages = [
        SeasonalAverage(month=m, avg_solar=round(sum(v) / len(v), 2) if v else 0.0)
        for m, v in seasonal.items()
    ]

    # YoY for ALL years in data
    years = sorted({r.year for r in energy_records})
    yoy = []
    for year in years:
        yr_records = [r for r in energy_records if r.year == year]
        total_solar = round(sum(r.solar for r in yr_records), 2)
        total_savings = 0.0
        if savings_by_month:
            total_savings = round(sum(s.value for s in savings_by_month if s.year == year), 2)
        yoy.append(YoYData(year=year, total_solar=total_solar, total_savings=total_savings))

    # ROI forecast: base / optimistic (+30%) / pessimistic (-30%)
    if len(yoy) >= 2:
        growth_rates = [
            (yoy[i].total_savings / yoy[i - 1].total_savings - 1)
            for i in range(1, len(yoy))
            if yoy[i - 1].total_savings > 0
        ]
        avg_growth = sum(growth_rates) / len(growth_rates) if growth_rates else 0.05
    else:
        avg_growth = 0.05

    base_savings = yoy[-1].total_savings if yoy else 0.0
    scenarios = [
        ROIScenario(
            year=i,
            base=round(base_savings * ((1 + avg_growth) ** i), 2),
            optimistic=round(base_savings * ((1 + avg_growth * 1.3) ** i), 2),
            pessimistic=round(base_savings * ((1 + avg_growth * 0.7) ** i), 2),
        )
        for i in range(1, 11)
    ]

    # MoM and YoY % for latest month
    sorted_records = sorted(energy_records, key=lambda x: (x.year, x.month), reverse=True)
    current = sorted_records[0]

    mom_solar = 0.0
    if len(sorted_records) > 1:
        prev = sorted_records[1]
        consecutive = (
            (current.year == prev.year and current.month == prev.month + 1) or
            (current.year == prev.year + 1 and current.month == 1 and prev.month == 12)
        )
        if consecutive and prev.solar > 0:
            mom_solar = round(((current.solar - prev.solar) / prev.solar) * 100, 1)

    yoy_solar = 0.0
    for r in sorted_records:
        if r.year == current.year - 1 and r.month == current.month:
            if r.solar > 0:
                yoy_solar = round(((current.solar - r.solar) / r.solar) * 100, 1)
            break

    return TrendsResult(
        seasonal_averages=seasonal_averages,
        year_over_year=yoy,
        roi_forecast=ROIForecast(scenarios=scenarios),
        yoy_solar_percent=yoy_solar,
        mom_solar_percent=mom_solar,
        data_points=len(energy_records),
    )
