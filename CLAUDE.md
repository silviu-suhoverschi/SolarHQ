# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**SolarHQ** is a Home Assistant addon that monitors solar energy installations and calculates financial performance (savings, ROI, payback period). It integrates with Home Assistant through the Supervisor API to auto-collect energy data from sensors.

**Current status**: Documentation and planning phase. See `APPLICATION_SPECS.md` (Romanian) and `IMPLEMENTATION_PLAN.md` for the full spec and code templates. No source code exists yet — both documents contain the full planned structure and sample implementations.

## Architecture

```
Frontend (Vue 3 SPA, hash mode)
        ↕ Axios → /api/*
FastAPI backend (port 8099) + APScheduler (hourly HA sync)
        ↕ SQLAlchemy async
SQLite (/data/db.sqlite3, WAL mode)
        ↕ httpx
Home Assistant Supervisor API (sensor discovery + LTS statistics)
```

All components run inside a single Docker container managed by **s6-overlay v3** with this startup order:

```
init-config → init-db (Alembic) → init-location → api + scheduler (parallel)
```

### Backend (`backend/`)

- `main.py` — FastAPI app with lifespan (startup/shutdown), mounts static frontend
- `config.py` — singleton `AppConfig` loaded from `/data/.env`
- `database.py` — async SQLAlchemy engine + session factory (aiosqlite)
- `ha_client.py` — httpx client for Supervisor API (sensor discovery, LTS stats fetch)
- `middleware.py` — validates Ingress X-Remote-User-* headers
- `models/` — SQLAlchemy ORM: `MonthlyEnergyRecord`, `Cost`, `SavingOffset`, `GridPrice`, `ProsumerPricing`, `AppConfig`
- `schemas/` — Pydantic v2 request/response models
- `routers/` — API endpoints: `dashboard`, `energy`, `costs`, `pricing`, `sensors`, `export`
- `services/` — pure financial calculation functions: `savings`, `roi`, `payback`, `projection`, `solar_price`, `self_consumption`, `export_income`, `capacity`, `trends`; `dashboard.py` orchestrates them all
- `tasks/` — APScheduler setup + `sync_energy_from_ha()` (fetches monthly LTS aggregates)
- `migrations/` — Alembic versions

### Frontend (`frontend/src/`)

- Vue Router in **hash mode** (required for HA Ingress prefix compatibility)
- Vite base URL set to `./` (relative, for Ingress)
- Views: `DashboardView`, `EnergyView`, `CostsView`, `PricingView`, `TrendsView`, `SettingsView`
- Pinia stores per domain (dashboard, energy, costs, pricing, etc.)
- Charts: ApexCharts via `vue3-apexcharts` in `components/charts/`
- KPI cards in `components/kpi/`

### HA Addon Infrastructure (`rootfs/`)

s6-overlay service scripts in `rootfs/etc/s6-overlay/s6-rc.d/` and entry points in `rootfs/usr/bin/`.

## Development Commands

### Frontend
```bash
cd frontend
npm install
npm run dev      # Dev server with hot reload
npm run build    # Production build → dist/
```

### Backend
```bash
cd backend
pip install -r requirements.txt
alembic upgrade head                          # Init/migrate DB
uvicorn main:app --reload --port 8099         # Dev server
```

### Docker (full addon build)
```bash
docker build -t solarhq:dev \
  --build-arg BUILD_FROM="ghcr.io/hassio-addons/base-python:3.11" \
  --build-arg BUILD_ARCH="amd64" \
  .
```

### Multi-arch build
```bash
docker buildx build \
  --platform linux/aarch64,linux/amd64,linux/arm/v7 \
  -t ghcr.io/yourusername/solarhq:1.0.0 \
  --push .
```

## Key Technical Decisions

- **SQLite WAL mode** at `/data/db.sqlite3` — persisted via HA's `/data` mount
- **Hash-mode Vue Router** — avoids Ingress path prefix conflicts
- **Relative Vite base (`./`)** — FastAPI serves the frontend at `/`, charts and assets resolve correctly under any Ingress path
- **APScheduler inside the FastAPI process** — not a separate service; runs the hourly HA sync
- **LTS statistics API** (`/api/history/period`) — fetches monthly kWh aggregates from HA Recorder; never raw sensor state
- **AppConfig singleton** (id=1 row in DB) — stores sensor entity mappings and last sync timestamp
- **Ingress auth** — `X-Remote-User` / `X-Remote-User-Display-Name` headers injected by HA; middleware enforces presence
- **`SUPERVISOR_TOKEN`** env var — injected automatically by HA; never logged

## Addon Options (set in HA Supervisor UI)

| Option | Values |
|--------|--------|
| `language` | ro / en / de / fr / es |
| `currency` | RON / EUR / USD / GBP |
| `log_level` | trace / debug / info / notice / warning / error / fatal |

## Financial Calculations

All implemented in `backend/services/` as pure functions taking ORM objects:

| Service | Formula |
|---------|---------|
| `savings.py` | `offset + Σ (consumption - import) × monthly_price` |
| `roi.py` | `(savings / investment) × 100` |
| `payback.py` | `investment / avg_monthly_savings` |
| `projection.py` | `avg_consumption × grid_price × 60` (5-year) |
| `solar_price.py` | `monthly_component_costs / avg_monthly_production` |
| `self_consumption.py` | `consumption - grid_import` (kWh + %) |
| `export_income.py` | `export_qty × export_price` |
| `capacity.py` | `annual_production / 1100` (kWp estimate) |
| `trends.py` | seasonal monthly averages + YoY comparison |

## Target Platforms

- aarch64 (Raspberry Pi 4)
- amd64 (NUC, VMs)
- armv7 (older Raspberry Pi)

Watchdog endpoint: `GET /health` → `{"status": "ok"}`
