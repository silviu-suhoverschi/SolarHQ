from __future__ import annotations
import os
import httpx
import logging

# Logger setup
logger = logging.getLogger(__name__)

# Supervisor details from environmental variables (provided by HA)
TOKEN = os.environ.get("SUPERVISOR_TOKEN")
HA_URL = "http://supervisor/core/api"

def _get_headers():
    return {
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json",
    }

async def get_ha_config() -> dict:
    """Fetch general Home Assistant configuration."""
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{HA_URL}/config", headers=_get_headers(), timeout=10.0)
        response.raise_for_status()
        return response.json()

async def discover_energy_sensors() -> dict[str, list[dict]]:
    """
    Discover all sensors with device_class 'energy' or 'power' and categorize them.
    Categorization is based on keyword heuristics in entity_id or friendly_name.
    """
    async with httpx.AsyncClient() as client:
        # User requested 30s timeout for states
        response = await client.get(f"{HA_URL}/states", headers=_get_headers(), timeout=30.0)
        response.raise_for_status()
        states = response.json()
        
        categories = {
            "solar": [],
            "import": [],
            "export": [],
            "battery": [],
            "load": [],
            "other": []
        }
        
        keywords = {
            "solar": ["solar", "pv", "photov", "produc"],
            "import": ["import", "grid", "retea", "cump"],
            "export": ["export", "inject", "vand", "vandut"],
            "battery": ["battery", "bateri", "acumul", "charge", "discharge"],
            "load": ["load", "consu", "house", "casa", "consum"]
        }
        
        for state in states:
            attr = state.get("attributes", {})
            device_class = attr.get("device_class")
            if device_class in ("energy", "power"):
                entity_id = state["entity_id"].lower()
                friendly_name = attr.get("friendly_name", "").lower()
                
                sensor_info = {
                    "entity_id": state["entity_id"],
                    "name": attr.get("friendly_name", state["entity_id"]),
                    "unit": attr.get("unit_of_measurement", "kWh")
                }
                
                matched = False
                for cat, keys in keywords.items():
                    if any(k in entity_id or k in friendly_name for k in keys):
                        categories[cat].append(sensor_info)
                        matched = True
                        break
                
                if not matched:
                    categories["other"].append(sensor_info)
                    
        return categories

async def get_monthly_statistics(entity_ids: list[str], start_time: str, end_time: str) -> list[dict]:
    """
    Fetch Long Term Statistics (LTS) for a list of entities.
    Aggregated by month.
    """
    if not entity_ids:
        return []

    payload = {
        "statistic_ids": entity_ids,
        "start_time": start_time,
        "end_time": end_time,
        "period": "month",
        "units": {"energy": "kWh"},
        "types": ["sum"],
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{HA_URL}/recorder/statistics_during_period",
            json=payload,
            headers=_get_headers(),
            timeout=30.0
        )
        response.raise_for_status()
        return response.json()
