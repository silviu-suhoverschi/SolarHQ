# Changelog

## [1.0.5] - 2026-03-27

### Fixed
- Add `cd /app` before `uvicorn` in `solarhq-api` — uvicorn could not find module `backend` without correct working directory
- Add `cd /app` and use `python3 -m backend.scripts.init_location` in `solarhq-location` — same root cause

## [1.0.4] - 2026-03-27

### Fixed
- Remove `bashio::addon.ingress_path` call from `solarhq-api` script — function does not exist in bashio; `INGRESS_PATH` was unused in backend

## [1.0.3] - 2026-03-27

### Fixed
- Replace `bashio::log.info` with `echo` in `solarhq-db` and `solarhq-location` scripts — bashio was not properly initialized in oneshot context causing `info: unbound variable` error

## [1.0.2] - 2026-03-27

### Fixed
- AppArmor profile: add `/init ix`, `file,` and `signal` rules to allow s6-overlay startup
- Alembic: remove `sqlalchemy.url` with configparser `%(DATA_PATH)s` interpolation from `alembic.ini` — URL is now always set from `database.py` which reads the `DATA_PATH` environment variable
- Hadolint: suppress `DL3029` warning for intentional `--platform=linux/amd64` on frontend build stage

## [1.0.1] - 2026-03-27

### Fixed
- Hadolint: suppress `DL3029` warning for `--platform` flag on frontend stage

## [1.0.0] - 2026-03-27

### Initial release
- Solar energy monitoring dashboard for Home Assistant
- Financial calculations: savings, ROI, payback period, 5-year projection
- Auto-sync energy data from Home Assistant sensors via Supervisor API (hourly)
- Multi-arch Docker images: amd64, aarch64, armv7
- Frontend: Vue 3 SPA with ApexCharts, Tailwind CSS v4, hash-mode router for HA Ingress
- Backend: FastAPI + SQLAlchemy async + SQLite WAL mode
- s6-overlay v3 service management with ordered startup
- Support for grid pricing, prosumer pricing, export income, self-consumption tracking
