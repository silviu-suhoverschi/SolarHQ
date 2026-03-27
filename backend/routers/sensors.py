from __future__ import annotations
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, status
from sqlalchemy.ext.asyncio import AsyncSession
from ..database import get_db
from ..models import AppConfig
from ..schemas.config import AppConfigUpdate, AppConfigResponse
from ..ha_client import discover_energy_sensors
from ..tasks.sync_energy import sync_energy_from_ha

router = APIRouter(prefix="/sensors", tags=["sensors"])

@router.get("/discover")
async def discover_sensors():
    """Discover energy-related sensors from Home Assistant."""
    return await discover_energy_sensors()

@router.get("/config", response_model=AppConfigResponse)
async def get_config(db: AsyncSession = Depends(get_db)):
    """Fetch current application configuration."""
    config = await db.get(AppConfig, 1)
    if not config:
        config = AppConfig(id=1)
        db.add(config)
        await db.commit()
        await db.refresh(config)
    return config

@router.post("/config", response_model=AppConfigResponse)
async def update_config(data: AppConfigUpdate, db: AsyncSession = Depends(get_db)):
    """Update application configuration."""
    config = await db.get(AppConfig, 1)
    if not config:
        config = AppConfig(id=1)
        db.add(config)
    
    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(config, key, value)
    
    return config

@router.post("/sync", status_code=status.HTTP_202_ACCEPTED)
async def trigger_sync(background_tasks: BackgroundTasks):
    """Manually trigger a background synchronization task."""
    background_tasks.add_task(sync_energy_from_ha)
    return {"message": "Synchronization task started in background."}
