# SolarHQ — Home Assistant App: Plan de Implementare

> **Data**: 2026-03-25
> **Stack**: FastAPI + SQLAlchemy + SQLite + Vue 3 + Vite + Tailwind + ApexCharts
> **Docs oficiale**: https://developers.home-assistant.io/docs/apps/

---

## Structura Proiectului

```
solarhq/
├── config.yaml
├── Dockerfile
├── build.yaml
├── apparmor.txt
├── CHANGELOG.md
├── DOCS.md
├── icon.png
├── logo.png
├── translations/
│   ├── en.yaml
│   └── ro.yaml
│
├── backend/
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   ├── ha_client.py
│   ├── middleware.py
│   ├── models/
│   ├── schemas/
│   ├── routers/
│   ├── services/
│   ├── tasks/
│   ├── scripts/
│   │   └── init_location.py
│   └── migrations/
│       └── versions/
│
├── frontend/
│   ├── index.html
│   ├── vite.config.js
│   ├── tailwind.config.js
│   ├── package.json
│   └── src/
│       ├── main.js
│       ├── App.vue
│       ├── router/
│       ├── stores/
│       ├── api/
│       ├── views/
│       └── components/
│
└── rootfs/
    ├── etc/s6-overlay/s6-rc.d/
    └── usr/bin/
```

---

## FAZA 1 — Infrastructura HA App

**Obiectiv**: App instalabil în HA, pornește, afișează logs.

### 1.1 Fișiere HA obligatorii

**`config.yaml`**
```yaml
name: "SolarHQ"
version: "1.0.0"
slug: "solarhq"
description: "Solar energy monitoring for Home Assistant"
url: "https://github.com/yourusername/solarhq-addon"
arch:
  - aarch64
  - amd64
  - armv7
init: false
startup: application
ingress: true
ingress_port: 8099
ingress_entry: "/"
panel_icon: "mdi:solar-power"
panel_title: "SolarHQ"
homeassistant_api: true
hassio_api: true
auth_api: true
watchdog: "http://[HOST]:[PORT:8099]/health"
map:
  - type: data
    read_only: false
options:
  log_level: "info"
  language: "ro"
  currency: "RON"
schema:
  log_level: "list(trace|debug|info|notice|warning|error|fatal)"
  language: "list(ro|en|de|fr|es)"
  currency: "list(RON|EUR|USD|GBP)"
```

**`build.yaml`**
```yaml
build_from:
  aarch64: "ghcr.io/hassio-addons/base-python:3.11"
  amd64: "ghcr.io/hassio-addons/base-python:3.11"
  armv7: "ghcr.io/hassio-addons/base-python:3.11"
```

**`repository.yaml`** (la rădăcina repository-ului)
```yaml
name: SolarHQ Repository
url: 'https://github.com/yourusername/solarhq-addon'
maintainer: Your Name <email>
```

### 1.2 Dockerfile

```dockerfile
# Stage 1 — build frontend
FROM node:20-alpine AS frontend-builder
WORKDIR /build
COPY frontend/package*.json frontend/vite.config.js frontend/tailwind.config.js ./
RUN npm ci
COPY frontend/ .
RUN npm run build

# Stage 2 — final image
ARG BUILD_FROM
FROM $BUILD_FROM

ARG BUILD_ARCH BUILD_DATE BUILD_DESCRIPTION BUILD_NAME BUILD_REF BUILD_REPOSITORY BUILD_VERSION

# Python deps
COPY backend/requirements.txt /app/backend/
RUN pip3 install --no-cache-dir -r /app/backend/requirements.txt

# App code
COPY backend/ /app/backend/
COPY --from=frontend-builder /build/dist/ /app/frontend/dist/

# s6-overlay scripts
COPY rootfs /
RUN chmod a+x /usr/bin/solarhq-*

LABEL \
    io.hass.name="${BUILD_NAME}" \
    io.hass.description="${BUILD_DESCRIPTION}" \
    io.hass.arch="${BUILD_ARCH}" \
    io.hass.type="addon" \
    io.hass.version="${BUILD_VERSION}" \
    org.opencontainers.image.title="${BUILD_NAME}" \
    org.opencontainers.image.source="https://github.com/${BUILD_REPOSITORY}" \
    org.opencontainers.image.created="${BUILD_DATE}" \
    org.opencontainers.image.revision="${BUILD_REF}" \
    org.opencontainers.image.version="${BUILD_VERSION}"
```

### 1.3 s6-overlay v3 — structura completă

```
rootfs/etc/s6-overlay/s6-rc.d/
├── user/
│   └── contents.d/          ← fișiere goale, activează serviciile
│       ├── init-config
│       ├── init-db
│       ├── init-location
│       ├── api
│       └── scheduler
├── init-config/
│   ├── type                 ← conținut: "oneshot"
│   ├── up                   ← path spre script
│   └── dependencies.d/
│       └── base             ← fișier gol
├── init-db/
│   ├── type
│   ├── up
│   └── dependencies.d/
│       └── init-config
├── init-location/
│   ├── type
│   ├── up
│   └── dependencies.d/
│       └── init-db
├── api/
│   ├── type                 ← conținut: "longrun"
│   ├── run
│   ├── finish
│   └── dependencies.d/
│       └── init-location
└── scheduler/
    ├── type
    ├── run
    ├── finish
    └── dependencies.d/
        └── init-location
```

**Scripts `/usr/bin/`:**

```bash
# solarhq-init (init-config)
#!/command/with-contenv bashio
[ ! -f /data/.secret_key ] && \
    python3 -c "import secrets; print(secrets.token_urlsafe(50))" > /data/.secret_key
{
    printf "SECRET_KEY=%s\n" "$(cat /data/.secret_key)"
    printf "LANGUAGE=%s\n"   "$(bashio::config 'language')"
    printf "CURRENCY=%s\n"   "$(bashio::config 'currency')"
    printf "LOG_LEVEL=%s\n"  "$(bashio::config 'log_level')"
} > /data/.env
mkdir -p /data/media /data/logs
bashio::log.info "Config OK"

# solarhq-db (init-db)
#!/command/with-contenv bashio
cd /app/backend && alembic upgrade head
bashio::log.info "DB OK"

# solarhq-location (init-location)
#!/command/with-contenv bashio
python3 /app/backend/scripts/init_location.py
bashio::log.info "Location OK"

# solarhq-api (api longrun)
#!/command/with-contenv bashio
INGRESS_PATH=$(bashio::addon.ingress_path)
export INGRESS_PATH
exec uvicorn backend.main:app --host 0.0.0.0 --port 8099 --workers 1

# solarhq-scheduler (scheduler longrun)
#!/command/with-contenv bashio
exec python3 /app/backend/tasks/scheduler.py
```

### 1.4 Test Faza 1
- [ ] App apare în HA → Settings → Apps → Local apps
- [ ] App pornește, logs vizibile
- [ ] Toate serviciile s6 pornesc în ordinea corectă
- [ ] `/health` returnează 200

---

## FAZA 2 — Backend: Database + Models

### 2.1 `backend/requirements.txt`
```
fastapi==0.135.2
uvicorn==0.42.0
sqlalchemy==2.0.48
aiosqlite==0.22.1
alembic==1.18.4
pydantic==2.12.5
apscheduler==3.11.2
httpx==0.28.1
cryptography==46.0.5
python-multipart==0.0.20
python-dotenv==1.1.0
```

### 2.2 `backend/database.py`
```python
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import event

engine = create_async_engine("sqlite+aiosqlite:////data/db.sqlite3")

@event.listens_for(engine.sync_engine, "connect")
def set_wal(conn, _):
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA synchronous=NORMAL")

SessionLocal = async_sessionmaker(engine, expire_on_commit=False)

class Base(DeclarativeBase):
    pass

async def get_db():
    async with SessionLocal() as s:
        yield s
```

### 2.3 Models

**`backend/models/energy.py`**
```python
class MonthlyEnergyRecord(Base):
    __tablename__ = "monthly_energy"
    id: Mapped[int] = mapped_column(primary_key=True)
    month: Mapped[date] = mapped_column(unique=True)
    solar: Mapped[float] = mapped_column(default=0)        # kWh produs
    load: Mapped[float] = mapped_column(default=0)         # kWh consumat
    grid_import: Mapped[float] = mapped_column(default=0)  # kWh cumpărat
    grid_export: Mapped[float] = mapped_column(default=0)  # kWh vândut
    battery_charge: Mapped[float] = mapped_column(default=0)
    battery_discharge: Mapped[float] = mapped_column(default=0)
```

**`backend/models/financial.py`**
```python
class Cost(Base):
    __tablename__ = "cost"
    id: Mapped[int] = mapped_column(primary_key=True)
    date: Mapped[date]
    description: Mapped[str]
    value: Mapped[float]
    currency: Mapped[str] = mapped_column(default="RON")
    operating_life_years: Mapped[int] = mapped_column(default=25)

class SavingOffset(Base):
    __tablename__ = "saving_offset"
    id: Mapped[int] = mapped_column(primary_key=True, default=1)
    value: Mapped[float] = mapped_column(default=0)
    currency: Mapped[str] = mapped_column(default="RON")

class GridPrice(Base):
    __tablename__ = "grid_price"
    id: Mapped[int] = mapped_column(primary_key=True)
    month: Mapped[date] = mapped_column(unique=True)
    price_per_kwh: Mapped[float]
    currency: Mapped[str] = mapped_column(default="RON")

class ProsumerPricing(Base):
    __tablename__ = "prosumer_pricing"
    id: Mapped[int] = mapped_column(primary_key=True)
    month: Mapped[date] = mapped_column(unique=True)
    import_price: Mapped[float]
    export_price: Mapped[float]
    fixed_tariff: Mapped[float] = mapped_column(default=0)
    tax: Mapped[float] = mapped_column(default=0)
    currency: Mapped[str] = mapped_column(default="RON")
```

**`backend/models/config.py`**
```python
class AppConfig(Base):
    """Configurare singleton — senzori HA + setări globale"""
    __tablename__ = "app_config"
    id: Mapped[int] = mapped_column(primary_key=True, default=1)
    location_name: Mapped[str] = mapped_column(default="My Home")
    currency: Mapped[str] = mapped_column(default="RON")
    sensor_solar: Mapped[str | None]       # entity_id senzor producție
    sensor_load: Mapped[str | None]        # entity_id senzor consum
    sensor_grid_import: Mapped[str | None]
    sensor_grid_export: Mapped[str | None]
    sensor_battery_charge: Mapped[str | None]
    sensor_battery_discharge: Mapped[str | None]
    last_sync: Mapped[datetime | None]
    sync_enabled: Mapped[bool] = mapped_column(default=True)
```

### 2.4 Alembic Setup
```bash
cd /app/backend
alembic init migrations
# Editare env.py să folosească SQLAlchemy async engine
alembic revision --autogenerate -m "initial"
```

### 2.5 Test Faza 2
- [ ] `alembic upgrade head` creează toate tabelele
- [ ] `/data/db.sqlite3` creat cu WAL mode
- [ ] `PRAGMA journal_mode` returnează `wal`

---

## FAZA 3 — Backend: FastAPI + HA Client

### 3.1 `backend/main.py`
```python
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from contextlib import asynccontextmanager
from .tasks.scheduler import start_scheduler
from .routers import dashboard, energy, costs, pricing, sensors, export

@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler = start_scheduler()
    yield
    scheduler.shutdown()

app = FastAPI(title="SolarHQ", version="1.0.0", lifespan=lifespan)

app.include_router(dashboard.router, prefix="/api")
app.include_router(energy.router,   prefix="/api")
app.include_router(costs.router,    prefix="/api")
app.include_router(pricing.router,  prefix="/api")
app.include_router(sensors.router,  prefix="/api")
app.include_router(export.router,   prefix="/api")

@app.get("/health")
async def health():
    return {"status": "ok"}

# Servire frontend Vue build
app.mount("/assets", StaticFiles(directory="/app/frontend/dist/assets"))

@app.get("/{full_path:path}")
async def spa(full_path: str):
    return FileResponse("/app/frontend/dist/index.html")
```

### 3.2 `backend/ha_client.py`
```python
import os, httpx

TOKEN = os.environ.get("SUPERVISOR_TOKEN")
HA_API = "http://supervisor/core/api"

def _h():
    return {"Authorization": f"Bearer {TOKEN}"}

async def get_ha_config() -> dict:
    async with httpx.AsyncClient() as c:
        return (await c.get(f"{HA_API}/config", headers=_h())).json()

async def discover_energy_sensors() -> list[dict]:
    """Returnează toți senzorii cu device_class energy sau power"""
    async with httpx.AsyncClient() as c:
        states = (await c.get(f"{HA_API}/states", headers=_h())).json()
    return [
        {"entity_id": s["entity_id"], "name": s["attributes"].get("friendly_name", s["entity_id"])}
        for s in states
        if s["attributes"].get("device_class") in ("energy", "power")
    ]

async def get_monthly_statistics(entity_ids: list[str], start: str, end: str) -> dict:
    """Long Term Statistics — agregate lunare kWh"""
    payload = {
        "statistic_ids": entity_ids,
        "start_time": start,
        "end_time": end,
        "period": "month",
        "units": {"energy": "kWh"},
        "types": ["sum"],
    }
    async with httpx.AsyncClient() as c:
        return (await c.post(f"{HA_API}/recorder/statistics_during_period",
                             json=payload, headers=_h())).json()
```

### 3.3 Middleware autentificare Ingress
```python
# backend/middleware.py
from starlette.middleware.base import BaseHTTPMiddleware

class HAAuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        request.state.user = {
            "id":           request.headers.get("X-Remote-User-Id"),
            "username":     request.headers.get("X-Remote-User-Name"),
            "display_name": request.headers.get("X-Remote-User-Display-Name"),
        }
        return await call_next(request)
```

### 3.4 Routers CRUD

Fiecare router urmează același pattern:

```python
# backend/routers/costs.py
router = APIRouter(prefix="/costs", tags=["costs"])

@router.get("/", response_model=list[CostSchema])
async def list_costs(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Cost).order_by(Cost.date.desc()))
    return result.scalars().all()

@router.post("/", response_model=CostSchema, status_code=201)
async def create_cost(data: CostCreate, db: AsyncSession = Depends(get_db)):
    cost = Cost(**data.model_dump())
    db.add(cost)
    await db.commit()
    await db.refresh(cost)
    return cost

@router.put("/{id}", response_model=CostSchema)
async def update_cost(id: int, data: CostCreate, db: AsyncSession = Depends(get_db)):
    ...

@router.delete("/{id}", status_code=204)
async def delete_cost(id: int, db: AsyncSession = Depends(get_db)):
    ...
```

Același pattern pentru: `energy`, `pricing/grid`, `pricing/prosumer`

### 3.5 Test Faza 3
- [ ] `GET /health` → 200
- [ ] `GET /api/costs` → listă goală `[]`
- [ ] `POST /api/costs` → creează înregistrare
- [ ] `GET /docs` → Swagger UI funcțional
- [ ] HA Client: `get_ha_config()` returnează date reale

---

## FAZA 4 — Servicii Financiare

### 4.1 Structura serviciilor

Fiecare serviciu este o funcție async pură care primește datele și returnează rezultatul:

```python
# backend/services/savings.py
async def calc_savings(
    energy_records: list[MonthlyEnergyRecord],
    grid_prices: list[GridPrice],
    offset: SavingOffset,
) -> dict:
    monthly = []
    for record in energy_records:
        price = _price_for_month(record.month, grid_prices)
        saved = (record.load - record.grid_import) * price
        monthly.append({"month": record.month, "saved": saved})
    total = offset.value + sum(m["saved"] for m in monthly)
    return {"total": total, "monthly": monthly, "currency": offset.currency}
```

### 4.2 Lista completă servicii

```
backend/services/
├── savings.py          calc_savings()         — economii totale + per lună
├── roi.py              calc_roi()             — ROI % + investiție totală
├── payback.py          calc_payback()         — luni până la amortizare
├── projection.py       calc_projection_5y()   — cost estimat fără solar 5 ani
├── solar_price.py      calc_solar_price()     — RON/kWh produs
├── self_consumption.py calc_self_consumption() — kWh + % autoconsum
├── export_income.py    calc_export_income()   — venit din vânzare energie
├── capacity.py         calc_capacity()        — kWp instalați estimat
├── trends.py           calc_trends()          — sezonier + YoY + prognoze ROI
└── dashboard.py        get_dashboard_data()   — orchestrator toate serviciile
```

### 4.3 `backend/routers/dashboard.py`

```python
@router.get("/dashboard")
async def get_dashboard(db: AsyncSession = Depends(get_db)):
    # Citire toate datele
    energy   = (await db.execute(select(MonthlyEnergyRecord))).scalars().all()
    costs    = (await db.execute(select(Cost))).scalars().all()
    prices   = (await db.execute(select(GridPrice))).scalars().all()
    prosumer = (await db.execute(select(ProsumerPricing))).scalars().all()
    offset   = await db.get(SavingOffset, 1) or SavingOffset()
    config   = await db.get(AppConfig, 1)

    return await get_dashboard_data(energy, costs, prices, prosumer, offset, config)
```

### 4.4 Test Faza 4
- [ ] `GET /api/dashboard` returnează toate câmpurile (cu date goale = 0)
- [ ] Adăugare câteva înregistrări test → valorile se calculează corect
- [ ] ROI = 0 când nu există costuri
- [ ] Serviciul trends returnează structura corectă

---

## FAZA 5 — Sincronizare HA

### 5.1 `backend/tasks/scheduler.py`

```python
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from .sync_energy import sync_energy_from_ha

def start_scheduler() -> AsyncIOScheduler:
    scheduler = AsyncIOScheduler()
    scheduler.add_job(sync_energy_from_ha, "interval", hours=1,
                      id="ha_sync", misfire_grace_time=300)
    scheduler.start()
    return scheduler
```

### 5.2 `backend/tasks/sync_energy.py`

```python
async def sync_energy_from_ha():
    async with SessionLocal() as db:
        config = await db.get(AppConfig, 1)
        if not config or not config.sync_enabled:
            return

        # Colectare entity_ids configurate
        sensors = {
            "solar":            config.sensor_solar,
            "load":             config.sensor_load,
            "grid_import":      config.sensor_grid_import,
            "grid_export":      config.sensor_grid_export,
            "battery_charge":   config.sensor_battery_charge,
            "battery_discharge":config.sensor_battery_discharge,
        }
        entity_ids = [v for v in sensors.values() if v]
        if not entity_ids:
            return

        # Fetch ultimele 13 luni din HA LTS
        end = datetime.now(UTC)
        start = end - timedelta(days=395)
        stats = await get_monthly_statistics(entity_ids, start.isoformat(), end.isoformat())

        # Transformare și salvare în DB
        for month_str, data in _aggregate_by_month(stats, sensors).items():
            month = date.fromisoformat(month_str)
            record = await db.get(MonthlyEnergyRecord, {"month": month})
            if not record:
                record = MonthlyEnergyRecord(month=month)
                db.add(record)
            # update câmpuri
            for field, value in data.items():
                setattr(record, field, value)

        config.last_sync = datetime.now(UTC)
        await db.commit()
```

### 5.3 `backend/routers/sensors.py`

```python
@router.get("/sensors/discover")
async def discover_sensors():
    """Listează toți senzorii energy/power din HA"""
    return await discover_energy_sensors()

@router.get("/sensors/config")
async def get_sensor_config(db: AsyncSession = Depends(get_db)):
    return await db.get(AppConfig, 1)

@router.post("/sensors/config")
async def save_sensor_config(data: SensorConfigSchema, db: AsyncSession = Depends(get_db)):
    config = await db.get(AppConfig, 1) or AppConfig(id=1)
    for field, value in data.model_dump(exclude_none=True).items():
        setattr(config, field, value)
    db.add(config)
    await db.commit()
    # Trigger sincronizare imediată
    await sync_energy_from_ha()
    return config

@router.post("/sensors/sync")
async def manual_sync():
    await sync_energy_from_ha()
    return {"status": "sync started"}
```

### 5.4 Test Faza 5
- [ ] `GET /api/sensors/discover` returnează senzorii din HA
- [ ] Salvare config senzori + trigger sync manual funcționează
- [ ] Date apar în `monthly_energy` după sync
- [ ] `last_sync` se actualizează corect

---

## FAZA 6 — Frontend Vue 3

### 6.1 Setup proiect

```bash
cd frontend
npm create vue@latest .    # Vue 3 + Vite + Vue Router + Pinia
npm install tailwindcss@4 axios vue3-apexcharts apexcharts
```

**`vite.config.js`**
```javascript
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  base: './',          // ← relativ, necesar pentru Ingress prefix
  build: { outDir: 'dist' }
})
```

**`frontend/src/api/index.js`**
```javascript
import axios from 'axios'
export default axios.create({ baseURL: '/api' })
```

### 6.2 Router (hash mode pentru Ingress)

```javascript
// src/router/index.js
import { createRouter, createWebHashHistory } from 'vue-router'
// Hash mode → URL: /api/hassio_ingress/abc123/#/dashboard
// Evită conflictul cu prefix-ul dinamic Ingress
export default createRouter({
  history: createWebHashHistory(),
  routes: [
    { path: '/',          redirect: '/dashboard' },
    { path: '/dashboard', component: () => import('@/views/DashboardView.vue') },
    { path: '/energy',    component: () => import('@/views/EnergyView.vue') },
    { path: '/costs',     component: () => import('@/views/CostsView.vue') },
    { path: '/pricing',   component: () => import('@/views/PricingView.vue') },
    { path: '/trends',    component: () => import('@/views/TrendsView.vue') },
    { path: '/settings',  component: () => import('@/views/SettingsView.vue') },
  ]
})
```

### 6.3 Pinia stores

```javascript
// src/stores/dashboard.js
import { defineStore } from 'pinia'
import api from '@/api'

export const useDashboardStore = defineStore('dashboard', {
  state: () => ({ data: null, loading: false }),
  actions: {
    async fetch() {
      this.loading = true
      this.data = (await api.get('/dashboard')).data
      this.loading = false
    }
  }
})
```

### 6.4 Componente grafice

```vue
<!-- src/components/charts/MonthlySavingsChart.vue -->
<template>
  <apexchart type="bar" :options="options" :series="series" height="300" />
</template>

<script setup>
import { computed } from 'vue'
const props = defineProps(['data'])

const series = computed(() => [{
  name: 'Economii',
  data: props.data?.monthly_savings?.map(m => m.value) ?? []
}])

const options = {
  chart: { toolbar: { show: false } },
  xaxis: { categories: props.data?.monthly_savings?.map(m => m.month) ?? [] },
  colors: ['#10b981'],
}
</script>
```

Același pattern pentru toate cele 9 grafice.

### 6.5 KPI Cards

```vue
<!-- src/components/kpi/ROICard.vue -->
<template>
  <div class="bg-white rounded-xl p-6 shadow-sm">
    <div class="text-sm text-gray-500">ROI</div>
    <div class="text-3xl font-bold text-green-600 mt-1">{{ roi }}%</div>
    <div class="text-sm text-gray-400 mt-1">Investiție: {{ cost }} RON</div>
  </div>
</template>

<script setup>
const props = defineProps(['roi', 'cost'])
</script>
```

### 6.6 Test Faza 6
- [ ] `npm run build` fără erori
- [ ] Frontend servit de FastAPI la `/`
- [ ] Navigare între toate paginile funcțională
- [ ] Dashboard afișează date din API
- [ ] Toate graficele se randează
- [ ] CRUD costuri funcțional din UI
- [ ] Pagina Setări: discover senzori + salvare + sync manual

---

## FAZA 7 — Testing & Securitate

### 7.1 `apparmor.txt`
```
#include <tunables/global>
profile solarhq flags=(attach_disconnected,mediate_deleted) {
  #include <abstractions/base>
  file,
  signal (send) set=(kill,term,int,hup,cont),
  /init ix,
  /bin/** ix,
  /usr/bin/** ix,
  /run/{s6,s6-rc*,service}/** ix,
  /command/** ix,
  /etc/s6-overlay/** rwix,
  /run/{,**} rwk,
  /usr/lib/bashio/** ix,
  /tmp/** rwk,
  /app/** r,
  /data/** rw,
  network inet tcp,
  network inet6 tcp,
}
```

### 7.2 Checklist testing

**Instalare & boot:**
- [ ] Instalare fresh pe HA curat → pornire fără erori
- [ ] `AppConfig` creat automat cu `location_name` din HA
- [ ] Toate serviciile s6 pornesc în ordinea corectă

**Update:**
- [ ] Update versiune app → datele din `/data/` se păstrează
- [ ] Migrații Alembic noi rulează automat la pornire

**Funcțional:**
- [ ] Adăugare costuri → ROI recalculat corect
- [ ] Adăugare prețuri rețea → economii recalculate
- [ ] Sync senzori HA → date apar în Energy view
- [ ] Export CSV descarcă fișier cu date corecte

**Ingress:**
- [ ] UI accesibil din sidebar HA
- [ ] Navigare Vue Router funcționează cu hash mode
- [ ] Assets (JS/CSS) se încarcă corect prin Ingress

**Securitate:**
- [ ] `SUPERVISOR_TOKEN` nu apare în logs
- [ ] AppArmor activ, app funcționează normal
- [ ] Memory idle < 128MB

---

## FAZA 8 — Documentație & Release

### 8.1 `DOCS.md`
- Instalare din repository
- Configurare options (limbă, monedă)
- Selectare senzori HA
- Adăugare costuri instalație
- Interpretare KPI-uri
- FAQ

### 8.2 `translations/en.yaml`
```yaml
configuration:
  log_level:
    name: Log Level
    description: Logging verbosity level.
  language:
    name: Language
    description: Interface language.
  currency:
    name: Currency
    description: Currency used for financial calculations.
```

### 8.3 CI/CD GitHub Actions
- `ci.yaml` — lint Dockerfile (hadolint), shellcheck scripts
- `deploy.yaml` — build multi-arch pe tag `v*` → push `ghcr.io`

### 8.4 Release
- [ ] Tag `v1.0.0`
- [ ] Testare instalare din URL repository extern
- [ ] Repository public

---

## Estimare Efort

| Faza | Zile |
|------|------|
| 1 — Infrastructura HA App | 3 |
| 2 — DB + Models | 2 |
| 3 — FastAPI + HA Client | 3 |
| 4 — Servicii financiare | 4 |
| 5 — Sincronizare HA | 2 |
| 6 — Frontend Vue 3 | 5 |
| 7 — Testing + Securitate | 3 |
| 8 — Docs + Release | 2 |
| **Total** | **~24 zile** |
