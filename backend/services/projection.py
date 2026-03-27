from __future__ import annotations
from ..schemas.services import ProjectionResult, YearProjection, MonthlySaving


async def calc_projection_5y(
    total_savings: float,
    monthly_savings: list[MonthlySaving],
) -> ProjectionResult:
    if not monthly_savings:
        return ProjectionResult(projected_savings_5y=0.0, projected_savings_10y=0.0, yearly=[])

    # Rolling 12-month average
    last_12 = monthly_savings[-12:] if len(monthly_savings) >= 12 else monthly_savings
    rolling_avg = sum(m.value for m in last_12) / len(last_12)
    annual = rolling_avg * 12

    yearly = [
        YearProjection(year=i, projected_savings=round(annual * i, 2))
        for i in range(1, 11)
    ]

    return ProjectionResult(
        projected_savings_5y=round(annual * 5, 2),
        projected_savings_10y=round(annual * 10, 2),
        yearly=yearly,
    )
