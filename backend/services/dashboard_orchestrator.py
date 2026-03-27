from __future__ import annotations
import asyncio
from . import (
    calc_savings, calc_roi, calc_payback, calc_projection_5y,
    calc_solar_price, calc_self_consumption, calc_export_income,
    calc_capacity,
)
from .trends import calc_trends
from ..schemas.dashboard import DashboardResponse


async def get_dashboard_data(
    energy_records: list,
    costs: list,
    grid_prices: list,
    prosumer_prices: list,
    offset,
    config,
) -> DashboardResponse:
    """Orchestrates all financial services. Single DB round-trip — data pre-fetched by router."""

    savings_r = await calc_savings(energy_records, grid_prices, offset)

    (
        roi_r, payback_r, projection_r,
        solar_price_r, self_cons_r, export_r, capacity_r,
    ) = await asyncio.gather(
        calc_roi(savings_r.total, costs),
        calc_payback(
            sum(c.value for c in costs),
            savings_r.total,
            savings_r.monthly,
        ),
        calc_projection_5y(savings_r.total, savings_r.monthly),
        calc_solar_price(energy_records, costs),
        calc_self_consumption(energy_records),
        calc_export_income(energy_records, prosumer_prices),
        calc_capacity(energy_records),
    )

    trends_r = await calc_trends(energy_records, savings_r.monthly)

    return DashboardResponse(
        savings=savings_r,
        roi=roi_r,
        payback=payback_r,
        projection=projection_r,
        solar_price=solar_price_r,
        self_consumption=self_cons_r,
        export_income=export_r,
        capacity=capacity_r,
        trends=trends_r,
        last_sync=config.last_sync if config else None,
        currency=config.currency if config else (offset.currency if offset else "RON"),
    )
