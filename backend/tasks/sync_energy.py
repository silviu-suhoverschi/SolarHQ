from __future__ import annotations
from datetime import datetime, UTC, timedelta
from sqlalchemy import select
from ..database import SessionLocal
from ..models import AppConfig, MonthlyEnergyRecord
from ..ha_client import get_monthly_statistics
import logging

logger = logging.getLogger(__name__)

async def sync_energy_from_ha():
    """Fetches missing or current energy data from Home Assistant LTS."""
    async with SessionLocal() as db:
        config = await db.get(AppConfig, 1)
        if not config or not config.sync_enabled:
            logger.info("Sync skipped: disabled or not configured.")
            return

        sensors = {
            "solar": config.sensor_solar,
            "load": config.sensor_load,
            "grid_import": config.sensor_grid_import,
            "grid_export": config.sensor_grid_export,
            "battery_charge": config.sensor_battery_charge,
            "battery_discharge": config.sensor_battery_discharge,
        }
        
        entity_ids = [v for v in sensors.values() if v]
        if not entity_ids:
            logger.info("Sync skipped: no sensors configured.")
            return

        # Fetch last 13 months
        end = datetime.now(UTC)
        start = end - timedelta(days=395)
        
        logger.info(f"Syncing energy for {len(entity_ids)} entities from {start.date()} to {end.date()}")
        
        try:
            stats_raw = await get_monthly_statistics(entity_ids, start.isoformat(), end.isoformat())
            monthly_data = _process_ha_stats(stats_raw, sensors)
            
            sync_time = datetime.now(UTC)
            
            for (year, month), data in monthly_data.items():
                stmt = select(MonthlyEnergyRecord).where(
                    MonthlyEnergyRecord.year == year,
                    MonthlyEnergyRecord.month == month
                )
                result = await db.execute(stmt)
                record = result.scalar_one_or_none()
                
                if not record:
                    record = MonthlyEnergyRecord(year=year, month=month)
                    db.add(record)
                
                # Update fields AND source/last_sync (Criteriu #3 & #4)
                record.source = "ha_sync"
                record.last_sync = sync_time
                
                for field, value in data.items():
                    setattr(record, field, value)
                
            config.last_sync = sync_time
            await db.commit()
            logger.info("Sync completed successfully.")
            
        except Exception as e:
            logger.error(f"Sync failed: {e}")

def _process_ha_stats(stats_raw: dict, sensors: dict) -> dict:
    processed = {}
    entity_to_field = {v: k for k, v in sensors.items() if v}
    
    for entity_id, stats in stats_raw.items():
        field = entity_to_field.get(entity_id)
        if not field: continue
        
        for entry in stats:
            dt = datetime.fromisoformat(entry["start"].replace("Z", "+00:00"))
            key = (dt.year, dt.month)
            if key not in processed: processed[key] = {}
            processed[key][field] = entry.get("sum", 0.0)
            
    return processed
