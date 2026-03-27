import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from .middleware import HAIngressMiddleware
from .tasks.scheduler import start_scheduler
from .routers import energy, costs, pricing, dashboard, sensors, export

# Lifespan for startup/shutdown events
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Start background scheduler
    scheduler = start_scheduler()
    print("SolarHQ Backend and Scheduler started.")
    yield
    # Shutdown scheduler
    scheduler.shutdown()
    print("SolarHQ Backend and Scheduler stopped.")

app = FastAPI(
    title="SolarHQ",
    version="1.0.3",
    lifespan=lifespan,
    docs_url="/api/docs",
    openapi_url="/api/openapi.json"
)

# Add HA Ingress Authentication Middleware
app.add_middleware(HAIngressMiddleware)

@app.get("/health")
async def health_check():
    return {"status": "ok", "version": "1.0.3"}

# Register Routers under /api
app.include_router(energy.router, prefix="/api")
app.include_router(costs.router, prefix="/api")
app.include_router(pricing.router, prefix="/api")
app.include_router(dashboard.router, prefix="/api")
app.include_router(sensors.router, prefix="/api")
app.include_router(export.router, prefix="/api")

# Static files for frontend
# Based on Acceptance Criteria: StaticFiles(html=True) for SPA fallback support
STATIC_PATH = "/app/static"

if os.path.exists(STATIC_PATH):
    # Mount static files at root / for SPA support
    # html=True enables automatic serving of index.html for directories
    app.mount("/", StaticFiles(directory=STATIC_PATH, html=True), name="frontend")
    
    # Catch-all route for SPA routing (redirect to index.html if not found)
    @app.exception_handler(404)
    async def spa_fallback(request, exc):
        if not request.url.path.startswith("/api"):
            return FileResponse(os.path.join(STATIC_PATH, "index.html"))
        return JSONResponse(status_code=404, content={"detail": "API Route Not Found"})

# Planned Router Imports (Faza 5+)
# from .routers import sensors, export
# app.include_router(sensors.router, prefix="/api")
# app.include_router(export.router, prefix="/api")
