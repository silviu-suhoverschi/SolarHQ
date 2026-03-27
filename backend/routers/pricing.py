from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional
from datetime import datetime

from ..database import get_db
from ..models import GridPrice, ProsumerPricing, SavingOffset
from ..schemas.pricing import (
    GridPriceCreate, GridPriceResponse,
    ProsumerPricingCreate, ProsumerPricingResponse,
    SavingOffsetBase, SavingOffsetResponse
)

router = APIRouter(prefix="/pricing", tags=["pricing"])

# --- Grid Pricing (Historical) ---
@router.get("/grid", response_model=list[GridPriceResponse])
async def list_grid_prices(year: Optional[int] = None, db: AsyncSession = Depends(get_db)):
    stmt = select(GridPrice)
    if year:
        stmt = stmt.where(GridPrice.year == year)
    stmt = stmt.order_by(GridPrice.year.desc(), GridPrice.month.desc())
    result = await db.execute(stmt)
    return result.scalars().all()

@router.post("/grid", response_model=GridPriceResponse, status_code=201)
async def create_grid_price(data: GridPriceCreate, db: AsyncSession = Depends(get_db)):
    # Check for duplicate
    stmt = select(GridPrice).where(
        GridPrice.year == data.year,
        GridPrice.month == data.month,
        GridPrice.time_of_use == data.time_of_use
    )
    result = await db.execute(stmt)
    if result.scalar_one_or_none():
        raise HTTPException(status_code=409, detail="Price already exists for this period and time-of-use")
    
    price = GridPrice(**data.model_dump())
    db.add(price)
    return price

# --- Prosumer Pricing ---
@router.get("/prosumer", response_model=list[ProsumerPricingResponse])
async def list_prosumer_pricing(year: Optional[int] = None, db: AsyncSession = Depends(get_db)):
    stmt = select(ProsumerPricing)
    if year:
        stmt = stmt.where(ProsumerPricing.year == year)
    stmt = stmt.order_by(ProsumerPricing.year.desc(), ProsumerPricing.month.desc())
    result = await db.execute(stmt)
    return result.scalars().all()

@router.post("/prosumer", response_model=ProsumerPricingResponse, status_code=201)
async def create_prosumer_pricing(data: ProsumerPricingCreate, db: AsyncSession = Depends(get_db)):
    stmt = select(ProsumerPricing).where(
        ProsumerPricing.year == data.year,
        ProsumerPricing.month == data.month
    )
    result = await db.execute(stmt)
    if result.scalar_one_or_none():
        raise HTTPException(status_code=409, detail="Pricing already exists for this period")
    
    pricing = ProsumerPricing(**data.model_dump())
    db.add(pricing)
    return pricing

# --- Savings Offset (Singleton) ---
@router.get("/savings-offset", response_model=SavingOffsetResponse)
async def get_saving_offset(db: AsyncSession = Depends(get_db)):
    offset = await db.get(SavingOffset, 1)
    if not offset:
        # Return default if not initialized
        return SavingOffset(id=1, value=0.0, currency="RON", created_at=datetime.now(), updated_at=datetime.now())
    return offset

@router.put("/savings-offset", response_model=SavingOffsetResponse)
async def update_saving_offset(data: SavingOffsetBase, db: AsyncSession = Depends(get_db)):
    offset = await db.get(SavingOffset, 1)
    if not offset:
        offset = SavingOffset(id=1)
    
    offset.value = data.value
    offset.currency = data.currency
    db.add(offset)
    return offset
