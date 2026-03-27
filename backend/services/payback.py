from __future__ import annotations
from ..schemas.services import PaybackResult, MonthlySaving


async def calc_payback(
    total_investment: float,
    total_savings: float,
    monthly_savings: list[MonthlySaving],
) -> PaybackResult:
    if total_investment <= 0:
        return PaybackResult(months_to_payback=0.0, estimated_date=None, status="no_investment")

    if total_savings >= total_investment:
        return PaybackResult(months_to_payback=0.0, estimated_date=None, status="paid_back")

    if not monthly_savings:
        return PaybackResult(months_to_payback=None, estimated_date=None, status="insufficient_data")

    avg_monthly = sum(m.value for m in monthly_savings) / len(monthly_savings)

    if avg_monthly <= 0:
        return PaybackResult(months_to_payback=None, estimated_date=None, status="no_savings")

    remaining = total_investment - total_savings
    months_remaining = remaining / avg_monthly

    return PaybackResult(
        months_to_payback=round(months_remaining, 1),
        estimated_date=None,
        status="remaining",
    )
