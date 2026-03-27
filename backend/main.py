from __future__ import annotations
import os
from contextlib import asynccontextmanager
from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from .middleware import HAIngressMiddleware
from .tasks.scheduler import start_scheduler
from .routers import energy, costs, pricing, dashboard, sensors, export

STATIC_PATH = "/app/static"
INDEX_HTML = os.path.join(STATIC_PATH, "index.html")

# Lifespan for startup/shutdown events
@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler = start_scheduler()
    print("SolarHQ Backend and Scheduler started.")
    yield
    scheduler.shutdown()
    print("SolarHQ Backend and Scheduler stopped.")

app = FastAPI(
    title="SolarHQ",
    version="1.0.11",
    lifespan=lifespan,
    docs_url="/api/docs",
    openapi_url="/api/openapi.json"
)

# Add HA Ingress Authentication Middleware
app.add_middleware(HAIngressMiddleware)

@app.get("/health")
async def health_check():
    return {"status": "ok", "version": "1.0.11"}

# Register Routers under /api
app.include_router(energy.router, prefix="/api")
app.include_router(costs.router, prefix="/api")
app.include_router(pricing.router, prefix="/api")
app.include_router(dashboard.router, prefix="/api")
app.include_router(sensors.router, prefix="/api")
app.include_router(export.router, prefix="/api")

# Serve index.html with X-Ingress-Path injected as window.BASE_URL
# Per HA docs: https://developers.home-assistant.io/docs/apps/presentation/
def _render_index(ingress_path: str) -> HTMLResponse:
    html = Path(INDEX_HTML).read_text()
    script = f'<script>window.BASE_URL="{ingress_path}";</script>'
    html = html.replace("</head>", f"{script}</head>")
    return HTMLResponse(html)

@app.get("/")
async def serve_index(request: Request):
    ingress_path = request.headers.get("X-Ingress-Path", "")
    return _render_index(ingress_path)

# Static assets (JS, CSS, images) — served directly
if os.path.exists(STATIC_PATH):
    app.mount("/", StaticFiles(directory=STATIC_PATH), name="frontend")

# SPA fallback for non-/api paths
@app.exception_handler(404)
async def spa_fallback(request: Request, exc):
    if not request.url.path.startswith("/api"):
        ingress_path = request.headers.get("X-Ingress-Path", "")
        return _render_index(ingress_path)
    return JSONResponse(status_code=404, content={"detail": "Not Found"})
