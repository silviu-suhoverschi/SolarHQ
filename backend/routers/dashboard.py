from __future__ import annotations
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from ..database import get_db
from ..models import MonthlyEnergyRecord, Cost, GridPrice, ProsumerPricing, SavingOffset, AppConfig
from ..services.dashboard_orchestrator import get_dashboard_data
from ..schemas.dashboard import DashboardResponse

router = APIRouter(prefix="/dashboard", tags=["dashboard"])

@router.get("/", response_model=DashboardResponse)
async def get_dashboard(db: AsyncSession = Depends(get_db)):
    """Fetch all metrics required for the main dashboard."""
    # Fetch all data concurrently/sequentially
    # (Since this is SQLite, sequential is safer/fine for this scale)
    energy_records = (await db.execute(select(MonthlyEnergyRecord))).scalars().all()
    costs = (await db.execute(select(Cost))).scalars().all()
    grid_prices = (await db.execute(select(GridPrice))).scalars().all()
    prosumer_prices = (await db.execute(select(ProsumerPricing))).scalars().all()
    
    offset = await db.get(SavingOffset, 1)
    config = await db.get(AppConfig, 1)
    
    return await get_dashboard_data(
        energy_records, 
        costs, 
        grid_prices, 
        prosumer_prices, 
        offset, 
        config
    )
