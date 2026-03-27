from __future__ import annotations
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from .sync_energy import sync_energy_from_ha

def start_scheduler() -> AsyncIOScheduler:
    """Initialize and start the background scheduler."""
    scheduler = AsyncIOScheduler()
    
    # Schedule energy sync every hour at minute 0
    # User requested CronTrigger(minute=0) and max_instances=1
    scheduler.add_job(
        sync_energy_from_ha, 
        trigger=CronTrigger(minute=0), 
        id="ha_sync", 
        max_instances=1,
        misfire_grace_time=300,
        coalesce=True
    )
    
    scheduler.start()
    return scheduler
