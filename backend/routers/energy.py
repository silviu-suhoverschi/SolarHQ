from __future__ import annotations
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from typing import Optional

from ..database import get_db
from ..models import MonthlyEnergyRecord
from ..schemas.energy import EnergyRecordCreate, EnergyRecordUpdate, EnergyRecordResponse

router = APIRouter(prefix="/energy", tags=["energy"])

@router.get("/", response_model=list[EnergyRecordResponse])
async def list_energy_records(
    year: Optional[int] = Query(None, ge=2000, le=2100),
    db: AsyncSession = Depends(get_db)
):
    """List all monthly energy records. Optional filtering by year."""
    stmt = select(MonthlyEnergyRecord)
    if year:
        stmt = stmt.where(MonthlyEnergyRecord.year == year)
    
    stmt = stmt.order_by(
        MonthlyEnergyRecord.year.desc(), 
        MonthlyEnergyRecord.month.desc()
    )
    
    result = await db.execute(stmt)
    return result.scalars().all()

@router.post("/", response_model=EnergyRecordResponse, status_code=status.HTTP_201_CREATED)
async def create_energy_record(data: EnergyRecordCreate, db: AsyncSession = Depends(get_db)):
    """Create a new energy record (manual entry)."""
    # Check for existing record
    stmt = select(MonthlyEnergyRecord).where(
        MonthlyEnergyRecord.year == data.year,
        MonthlyEnergyRecord.month == data.month
    )
    result = await db.execute(stmt)
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Record already exists for {data.year}-{data.month:02d}"
        )

    record = MonthlyEnergyRecord(**data.model_dump())
    db.add(record)
    return record

@router.get("/{id}", response_model=EnergyRecordResponse)
async def get_energy_record(id: int, db: AsyncSession = Depends(get_db)):
    """Get a specific energy record by ID."""
    record = await db.get(MonthlyEnergyRecord, id)
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")
    return record

@router.put("/{id}", response_model=EnergyRecordResponse)
async def update_energy_record(id: int, data: EnergyRecordUpdate, db: AsyncSession = Depends(get_db)):
    """Update an existing energy record."""
    record = await db.get(MonthlyEnergyRecord, id)
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")
    
    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(record, key, value)
    
    return record

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_energy_record(id: int, db: AsyncSession = Depends(get_db)):
    """Delete an energy record."""
    record = await db.get(MonthlyEnergyRecord, id)
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")
    
    await db.delete(record)
    return None
