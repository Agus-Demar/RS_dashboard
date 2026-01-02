"""
FastAPI application entry point.

Main application that:
- Serves the REST API endpoints
- Mounts the Plotly Dash dashboard
- Initializes the database
- Optionally starts the scheduler
"""
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from src.config import settings
from src.models import init_db
from src.api.routes import rs_router, gics_router, health_router
from src.dashboard.app import create_dash_app

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan handler.
    
    Runs on startup and shutdown.
    """
    # Startup
    logger.info("Starting RS Dashboard application...")
    
    # Initialize database
    logger.info("Initializing database...")
    init_db()
    
    # Start scheduler if enabled
    if settings.SCHEDULER_ENABLED:
        try:
            from src.jobs.scheduler import start_scheduler
            start_scheduler()
            logger.info("Scheduler started")
        except ImportError:
            logger.warning("Scheduler module not available")
        except Exception as e:
            logger.error(f"Failed to start scheduler: {e}")
    
    logger.info("Application startup complete")
    
    yield
    
    # Shutdown
    logger.info("Shutting down application...")
    
    if settings.SCHEDULER_ENABLED:
        try:
            from src.jobs.scheduler import stop_scheduler
            stop_scheduler()
            logger.info("Scheduler stopped")
        except Exception as e:
            logger.warning(f"Error stopping scheduler: {e}")


# Create FastAPI app
app = FastAPI(
    title="RS Dashboard API",
    description="Relative Strength Industry Dashboard - REST API and Interactive Visualization",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(health_router)
app.include_router(rs_router, prefix="/api")
app.include_router(gics_router, prefix="/api")

# Mount Dash app
# routes_pathname_prefix="/": Flask sees requests at root (after WSGI strips /dashboard)
# requests_pathname_prefix="/dashboard/": Browser requests include /dashboard/ prefix
dash_app = create_dash_app(
    routes_pathname_prefix="/",
    requests_pathname_prefix="/dashboard/"
)

# For FastAPI + Dash integration, we use the WSGI middleware
from starlette.middleware.wsgi import WSGIMiddleware
app.mount("/dashboard", WSGIMiddleware(dash_app.server))


@app.get("/", include_in_schema=False)
async def root():
    """Redirect root to dashboard."""
    return RedirectResponse(url="/dashboard/")


@app.get("/api", include_in_schema=False)
async def api_root():
    """API information endpoint."""
    return {
        "name": "RS Dashboard API",
        "version": "1.0.0",
        "docs": "/api/docs",
        "dashboard": "/dashboard/",
        "endpoints": {
            "rs_matrix": "/api/rs/matrix",
            "gics_sectors": "/api/gics/sectors",
            "health": "/health",
            "status": "/api/status",
        }
    }


def run_dev_server(host: str = "0.0.0.0", port: int = 8000, reload: bool = True):
    """
    Run development server.
    
    Args:
        host: Host to bind to
        port: Port to run on
        reload: Enable auto-reload
    """
    import uvicorn
    uvicorn.run(
        "src.main:app",
        host=host,
        port=port,
        reload=reload,
        log_level=settings.LOG_LEVEL.lower()
    )


if __name__ == "__main__":
    run_dev_server()

