"""
Dash application initialization.

Creates and configures the Plotly Dash application for the RS Dashboard.
"""
import os
from typing import Optional

from dash import Dash
import dash_bootstrap_components as dbc

from src.dashboard.layouts.main_layout import create_layout
from src.dashboard.callbacks import register_callbacks

# Get the assets folder path relative to this file
ASSETS_PATH = os.path.join(os.path.dirname(__file__), "assets")


def create_dash_app(server=None, routes_pathname_prefix: str = "/", requests_pathname_prefix: str = "/dashboard/") -> Dash:
    """
    Create and configure the Plotly Dash application.
    
    Args:
        server: Optional Flask server to mount on. If None, creates its own Flask server.
        routes_pathname_prefix: Prefix for Flask routes (internal)
        requests_pathname_prefix: Prefix for browser requests (external URLs)
    
    Returns:
        Configured Dash application
    """
    # If no server provided, let Dash create its own Flask server
    if server is None:
        server = True
    
    # Create Dash app
    # routes_pathname_prefix: what Flask sees internally
    # requests_pathname_prefix: what the browser requests (includes /dashboard mount point)
    app = Dash(
        __name__,
        server=server,
        routes_pathname_prefix=routes_pathname_prefix,
        requests_pathname_prefix=requests_pathname_prefix,
        assets_folder=ASSETS_PATH,  # Custom assets folder path
        external_stylesheets=[
            dbc.themes.DARKLY,  # Dark Bootstrap theme
            dbc.icons.FONT_AWESOME,  # Icons
        ],
        suppress_callback_exceptions=True,
        title="RS Industry Dashboard",
        update_title="Loading...",
    )
    
    # Set layout
    app.layout = create_layout()
    
    # Register callbacks
    register_callbacks(app)
    
    return app


def run_standalone(debug: bool = True, port: int = 8050):
    """
    Run the dashboard as a standalone application.
    
    Args:
        debug: Enable debug mode
        port: Port to run on
    """
    app = create_dash_app(routes_pathname_prefix="/", requests_pathname_prefix="/")
    app.run(debug=debug, port=port)


if __name__ == "__main__":
    run_standalone()

