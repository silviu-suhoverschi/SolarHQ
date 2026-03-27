import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse, FileResponse
from .middleware import HAIngressMiddleware

# Lifespan for startup/shutdown events
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Prepare things here (e.g. start scheduler later in Phase 5)
    print("SolarHQ Backend starting...")
    yield
    print("SolarHQ Backend shutting down...")

app = FastAPI(
    title="SolarHQ",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/api/docs",
    openapi_url="/api/openapi.json"
)

# Add HA Ingress Authentication Middleware
app.add_middleware(HAIngressMiddleware)

@app.get("/health")
async def health_check():
    return {"status": "ok", "version": "1.0.0"}

# Static files for frontend
# Based on Dockerfile criteria #1: Frontend copied to /app/static
STATIC_PATH = "/app/static"

if os.path.exists(STATIC_PATH):
    app.mount("/static", StaticFiles(directory=STATIC_PATH), name="static")

    @app.get("/{full_path:path}")
    async def serve_spa(request: Request, full_path: str):
        # Serve index.html for all non-api routes to support SPA routing
        if full_path.startswith("api"):
            return JSONResponse(status_code=404, content={"detail": "Not Found"})
        
        index_file = os.path.join(STATIC_PATH, "index.html")
        if os.path.exists(index_file):
            return FileResponse(index_file)
        return JSONResponse(status_code=404, content={"detail": "Frontend not found"})
else:
    @app.get("/")
    async def root():
        return {"message": "SolarHQ API is running. Frontend not found at /app/static."}
