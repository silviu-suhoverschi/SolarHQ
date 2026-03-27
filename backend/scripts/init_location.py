from __future__ import annotations
"""
Seed AppConfig with HA location name and currency on first boot.
Called by s6 init-location oneshot service.
"""
import asyncio
import sys
import os

import httpx

sys.path.insert(0, os.path.realpath(os.path.join(os.path.dirname(__file__), '..', '..')))

from backend.database import SessionLocal
from backend.models import AppConfig

SUPERVISOR_TOKEN = os.environ["SUPERVISOR_TOKEN"]
CURRENCY = os.environ.get("CURRENCY", "RON")
LANGUAGE = os.environ.get("LANGUAGE", "ro")


async def get_ha_config() -> dict:
    async with httpx.AsyncClient() as client:
        resp = await client.get(
            "http://supervisor/core/api/config",
            headers={"Authorization": f"Bearer {SUPERVISOR_TOKEN}"},
            timeout=10.0,
        )
        resp.raise_for_status()
        return resp.json()


async def init_location():
    ha_cfg = await get_ha_config()
    location_name = ha_cfg.get("location_name", "Home")

    async with SessionLocal() as session:
        config = await session.get(AppConfig, 1)
        if config is None:
            config = AppConfig(id=1)
            session.add(config)
        config.location_name = location_name
        config.currency = CURRENCY
        config.language = LANGUAGE
        await session.commit()

    print(f"Location seeded: {location_name} / {CURRENCY} / {LANGUAGE}")


if __name__ == "__main__":
    try:
        asyncio.run(init_location())
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)
