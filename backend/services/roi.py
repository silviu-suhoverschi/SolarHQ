from ..models import Cost
from ..schemas.services import ROIResult


async def calc_roi(
    total_savings: float,
    costs: list[Cost],
) -> ROIResult:
    total_investment = sum(c.value for c in costs)

    if total_investment == 0:
        return ROIResult(roi_percent=0.0, total_investment=0.0)

    roi_percent = ((total_savings - total_investment) / total_investment) * 100

    return ROIResult(
        roi_percent=round(roi_percent, 2),
        total_investment=round(total_investment, 2),
    )
