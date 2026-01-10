"""
FastAPI application entry point.

Main application that:
- Serves the REST API endpoints
- Mounts the Plotly Dash dashboard
- Initializes the database
- Checks data freshness on startup (runs update if stale)
- Optionally starts the scheduler
"""
import logging
from contextlib import asynccontextmanager
from datetime import date

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


def check_and_update_data() -> None:
    """
    Check if data is up to date with the last complete week.
    
    If the latest RS data is older than the last complete week (Friday),
    runs the weekly data update job to fill the gap.
    """
    from src.models import SessionLocal
    from src.services.aggregator import get_last_friday
    from src.services.data_service import get_latest_available_week
    
    logger.info("Checking data freshness...")
    
    db = SessionLocal()
    try:
        # Get the last complete week (most recent Friday)
        last_friday = get_last_friday()
        
        # Get the latest RS data in the database
        latest_rs_week = get_latest_available_week(db)
        
        if latest_rs_week is None:
            logger.warning("No RS data found in database. Please run initial data load.")
            return
        
        logger.info(f"Last complete week: {last_friday}")
        logger.info(f"Latest RS data: {latest_rs_week}")
        
        # Check if we need to update
        if latest_rs_week < last_friday:
            logger.info(f"Data is stale (missing {(last_friday - latest_rs_week).days} days). Running update...")
            
            # Calculate how many days of price data to fetch
            days_gap = (date.today() - latest_rs_week).days + 1
            days_to_fetch = max(7, days_gap)  # At least 7 days
            
            # Run the unified weekly update job
            from src.jobs.weekly_rs_job import run_weekly_data_update
            result = run_weekly_data_update()
            
            if result.get('success'):
                logger.info(f"Data update complete: {result.get('rs_records_processed', 0)} RS records updated")
            else:
                logger.error(f"Data update failed: {result.get('error')}")
        else:
            logger.info("Data is up to date!")
            
    except Exception as e:
        logger.error(f"Error checking data freshness: {e}")
    finally:
        db.close()


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
    
    # Check data freshness and update if needed
    try:
        check_and_update_data()
    except Exception as e:
        logger.error(f"Error during data freshness check: {e}")
    
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

