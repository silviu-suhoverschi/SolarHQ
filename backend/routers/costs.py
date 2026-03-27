from __future__ import annotations
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from datetime import date
from typing import Optional

from ..database import get_db
from ..models import Cost
from ..schemas.costs import CostCreate, CostUpdate, CostResponse

router = APIRouter(prefix="/costs", tags=["costs"])

@router.get("/", response_model=list[CostResponse])
async def list_costs(
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    db: AsyncSession = Depends(get_db)
):
    """List all infrastructure/installation costs."""
    stmt = select(Cost)
    if start_date:
        stmt = stmt.where(Cost.date >= start_date)
    if end_date:
        stmt = stmt.where(Cost.date <= end_date)
    
    stmt = stmt.order_by(Cost.date.desc())
    result = await db.execute(stmt)
    return result.scalars().all()

@router.post("/", response_model=CostResponse, status_code=status.HTTP_201_CREATED)
async def create_cost(data: CostCreate, db: AsyncSession = Depends(get_db)):
    """Add a new cost item. Prevents duplicate year/month/description entries."""
    # The user requested a duplicate check for year/month in costs.
    # Since Cost uses a full date, we'll check for same date + description.
    stmt = select(Cost).where(
        Cost.date == data.date,
        Cost.description == data.description,
        Cost.value == data.value
    )
    result = await db.execute(stmt)
    if result.scalar_one_or_none():
        raise HTTPException(status_code=409, detail="Identical cost entry already exists for this date")
    
    cost = Cost(**data.model_dump())
    db.add(cost)
    return cost

@router.get("/{id}", response_model=CostResponse)
async def get_cost(id: int, db: AsyncSession = Depends(get_db)):
    """Get a specific cost item."""
    cost = await db.get(Cost, id)
    if not cost:
        raise HTTPException(status_code=404, detail="Cost item not found")
    return cost

@router.put("/{id}", response_model=CostResponse)
async def update_cost(id: int, data: CostUpdate, db: AsyncSession = Depends(get_db)):
    """Update an existing cost item."""
    cost = await db.get(Cost, id)
    if not cost:
        raise HTTPException(status_code=404, detail="Cost item not found")
    
    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(cost, key, value)
    
    return cost

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_cost(id: int, db: AsyncSession = Depends(get_db)):
    """Delete a cost item."""
    cost = await db.get(Cost, id)
    if not cost:
        raise HTTPException(status_code=404, detail="Cost item not found")
    
    await db.delete(cost)
    return None
