import csv
import io
from fastapi import APIRouter, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, extract
from ..database import get_db
from ..models import MonthlyEnergyRecord, Cost

router = APIRouter(prefix="/export", tags=["export"])

@router.get("/csv")
async def export_csv(db: AsyncSession = Depends(get_db)):
    """Export all energy records to a CSV file with calculated fields and costs."""
    # Order ascending as requested
    stmt = select(MonthlyEnergyRecord).order_by(
        MonthlyEnergyRecord.year.asc(), 
        MonthlyEnergyRecord.month.asc()
    )
    result = await db.execute(stmt)
    records = result.scalars().all()
    
    # Fetch all costs to associate
    costs_result = await db.execute(select(Cost))
    all_costs = costs_result.scalars().all()
    
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Header
    writer.writerow([
        "Year", "Month", "Solar (kWh)", "Load (kWh)", 
        "Grid Import (kWh)", "Grid Export (kWh)", 
        "Battery Charge (kWh)", "Battery Discharge (kWh)",
        "Self Consumed (kWh)", "Self Consumption %",
        "Cost Value", "Cost Currency",
        "Source", "Last Sync"
    ])
    
    # Data
    for r in records:
        # Calculate fields
        self_consumed = max(0, r.load - r.grid_import)
        self_consumption_pct = (self_consumed / r.solar * 100) if r.solar > 0 else 0
        
        # Find cost for this year/month (Simplified: finding any cost on exactly that year/month or summing them)
        month_costs = [c for c in all_costs if c.date.year == r.year and c.date.month == r.month]
        cost_val = sum(c.value for c in month_costs) if month_costs else ""
        cost_curr = month_costs[0].currency if month_costs else ""
        
        writer.writerow([
            r.year, r.month, r.solar, r.load, 
            r.grid_import, r.grid_export, 
            r.battery_charge or 0, r.battery_discharge or 0,
            round(self_consumed, 2), round(self_consumption_pct, 1),
            cost_val, cost_curr,
            r.source, r.last_sync
        ])
    
    content = output.getvalue()
    return Response(
        content=content,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=solarhq_export.csv"}
    )
