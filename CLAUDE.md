# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**SolarHQ** is a Home Assistant addon that monitors solar energy installations and calculates financial performance (savings, ROI, payback period). It integrates with Home Assistant through the Supervisor API to auto-collect energy data from sensors.

**Current status**: Source code fully implemented and building successfully. Multi-arch Docker images published to `ghcr.io/silviu-suhoverschi/solarhq/{arch}` via GitHub Actions.

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
init-config → init-db (Alembic) → init-location → solarhq-api + solarhq-scheduler (parallel)
```

### Backend (`backend/`)

- `main.py` — FastAPI app with lifespan (startup/shutdown), mounts static frontend at `/app/static`
- `__main__.py` — entry point for `python3 -m backend`
- `database.py` — async SQLAlchemy engine + session factory (aiosqlite), WAL mode
- `ha_client.py` — httpx client for Supervisor API (sensor discovery, LTS stats fetch)
- `middleware.py` — validates Ingress `X-Remote-User-*` headers
- `models/` — SQLAlchemy ORM: `MonthlyEnergyRecord`, `Cost`, `SavingOffset`, `GridPrice`, `ProsumerPricing`, `AppConfig`
- `schemas/` — Pydantic v2 request/response models
- `routers/` — API endpoints: `dashboard`, `energy`, `costs`, `pricing`, `sensors`, `export`
- `services/` — pure financial calculation functions (see table below); `dashboard_orchestrator.py` aggregates them
- `tasks/scheduler.py` — APScheduler setup; `tasks/sync_energy.py` — `sync_energy_from_ha()`; run via `python3 -m backend.tasks`
- `migrations/` — Alembic versions (0001 initial, 0002 add_last_sync)
- `scripts/init_location.py` — one-shot script to set location from HA config

### Frontend (`frontend/src/`)

- Vue Router in **hash mode** (required for HA Ingress prefix compatibility)
- Vite 8 (rolldown) with `base: './'` and `outDir: '../static'` — builds into `/static/` at repo root
- Tailwind CSS v4 via `@tailwindcss/vite` plugin (no `tailwind.config.js` needed)
- Views: `DashboardView`, `EnergyView`, `CostsView`, `PricingView`, `TrendsView`, `SettingsView`
- Pinia stores: `dashboard.js`, `energy.js`, `costs.js`, `pricing.js`, `settings.js`
- Charts: 9 ApexCharts components in `components/charts/`
- KPI cards: 7 components in `components/kpi/`
- `components/SensorSelect.vue` — reusable sensor entity picker
- `utils/csvExport.js` — CSV download via blob URL

### HA Addon Infrastructure (`rootfs/`)

- `rootfs/usr/bin/` — entry point scripts: `solarhq-api`, `solarhq-scheduler`, `solarhq-db`, `solarhq-init`, `solarhq-location`
- `rootfs/etc/s6-overlay/s6-rc.d/` — s6 service definitions with dependency ordering
- `rootfs/etc/s6-overlay/s6-rc.d/user/contents.d/` — lists all services in the user bundle

## Development Commands

### Frontend
```bash
cd frontend
npm install
npm run dev      # Dev server on :3000 with /api proxy → :8099
npm run build    # Production build → ../static/
```

### Backend
```bash
cd backend
pip install -r requirements.txt
alembic upgrade head                           # Init/migrate DB
uvicorn backend.main:app --reload --port 8099  # Dev server (run from repo root)
```

### Docker (local amd64 test build)
```bash
docker build -t solarhq:dev \
  --build-arg BUILD_FROM="ghcr.io/home-assistant/amd64-base-python:latest" \
  --build-arg BUILD_ARCH="amd64" \
  .
```

## CI/CD

- **`.github/workflows/ci.yaml`** — runs on every push: hadolint, shellcheck, YAML lint, pytest
- **`.github/workflows/deploy.yaml`** — triggers on `v*` tags; builds and pushes multi-arch images to ghcr.io
- Deploy matrix: `amd64` (linux/amd64), `aarch64` (linux/arm64), `armv7` (linux/arm/v7)
- After build, `update-build-yaml` job pins the version in `build.yaml` and commits back to main
- Images published to: `ghcr.io/silviu-suhoverschi/solarhq/{arch}:{version}`

## Key Technical Decisions

- **SQLite WAL mode** at `/data/db.sqlite3` — persisted via HA's `/data` mount
- **Hash-mode Vue Router** — avoids Ingress path prefix conflicts
- **Relative Vite base (`./`)** — FastAPI serves the frontend at `/`, assets resolve correctly under any Ingress path
- **Frontend build forced to `linux/amd64`** — rolldown (Vite 8's Rust bundler) has no `linux-arm-musleabihf` binding; frontend stage uses `FROM --platform=linux/amd64 node:20-alpine`, final image is still the correct target arch
- **`npm install` (not `npm ci`)** in Dockerfile — avoids lockfile arch mismatch for optional native deps
- **`python3 -m backend.tasks`** for scheduler — avoids relative import errors when running as a script
- **APScheduler inside the FastAPI process** — not a separate service; scheduler runs as a separate s6 service calling `python3 -m backend.tasks`
- **LTS statistics API** (`/api/history/period`) — fetches monthly kWh aggregates from HA Recorder; never raw sensor state
- **AppConfig singleton** (id=1 row in DB) — stores sensor entity mappings and last sync timestamp
- **Ingress auth** — `X-Remote-User` / `X-Remote-User-Display-Name` headers injected by HA; middleware enforces presence
- **`SUPERVISOR_TOKEN`** env var — injected automatically by HA; never logged
- **pydantic>=2.11.0** — required for Python 3.14 support (PyO3 ≥ 0.24); also needs `build-base libffi-dev rust cargo` in apk for compilation
- **Hadolint suppressions**: `DL3006` on `FROM $BUILD_FROM` (dynamic base), `DL3018` on apk installs, `DL3029` on `--platform` override for frontend stage

## Addon Options (set in HA Supervisor UI)

| Option | Values |
|--------|--------|
| `language` | ro / en / de / fr / es |
| `currency` | RON / EUR / USD / GBP |
| `log_level` | trace / debug / info / notice / warning / error / fatal |

Translations for these options: `translations/en.yaml`, `translations/ro.yaml`

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

- aarch64 (Raspberry Pi 4) — primary target
- amd64 (NUC, VMs)
- armv7 (older Raspberry Pi)

Base images: `ghcr.io/home-assistant/{arch}-base-python:latest`

Watchdog endpoint: `GET /health` → `{"status": "ok"}`
