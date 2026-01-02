"""
API routes.
"""
from src.api.routes.rs import router as rs_router
from src.api.routes.gics import router as gics_router
from src.api.routes.health import router as health_router

__all__ = ["rs_router", "gics_router", "health_router"]

