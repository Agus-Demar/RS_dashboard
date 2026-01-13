"""
Ticker searcher page callbacks.

Handles:
- Ticker search and lookup
- Sub-industry heatmap generation for the found ticker's sub-industry
- Price chart with RS indicator display
"""
import logging
from typing import Optional

import pandas as pd
import plotly.graph_objects as go
from dash import callback, Input, Output, State, html, no_update, ctx
import dash_bootstrap_components as dbc

from src.models import SessionLocal, Stock
from src.services.data_service import (
    get_stock_rs_matrix_data,
    get_subindustry_info,
    get_stock_price_with_rs,
    get_stock_price_with_rs_weekly,
)
from src.dashboard.callbacks.stock_callbacks import (
    create_stock_heatmap_figure,
    create_price_rs_chart,
)
from src.dashboard.utils.colors import get_strength_label
from src.dashboard.utils.heatmap_config import COLORS

logger = logging.getLogger(__name__)


def register_ticker_callbacks(app):
    """Register all callbacks for the ticker searcher page."""
    
    @app.callback(
        Output("ticker-search-result", "children"),
        Output("ticker-subindustry-code", "data"),
        Output("ticker-controls-container", "style"),
        Output("ticker-heatmap-container", "style"),
        Output("ticker-detail-container", "style"),
        Output("ticker-chart-container", "style"),
        Output("ticker-chart-title", "children"),
        Output("ticker-price-rs-chart", "figure"),
        Output("ticker-selected-stock-store", "data"),
        Input("ticker-search-button", "n_clicks"),
        Input("ticker-search-input", "n_submit"),
        Input("ticker-search-value", "data"),
        State("ticker-search-input", "value"),
    )
    def search_ticker(n_clicks, n_submit, initial_ticker, search_value):
        """Handle ticker search and display initial results."""
        
        # Hidden styles
        hidden_style = {"display": "none"}
        visible_style = {"display": "block"}
        chart_visible_style = {"display": "block", "marginTop": "2.5rem", "paddingTop": "1rem"}
        
        # Empty figure for initial state
        empty_fig = go.Figure()
        empty_fig.update_layout(
            paper_bgcolor=COLORS["paper_bg"],
            plot_bgcolor=COLORS["plot_bg"],
            font=dict(color=COLORS["text"]),
        )
        
        # Determine the ticker to search
        triggered_id = ctx.triggered_id if ctx.triggered_id else None
        
        if triggered_id == "ticker-search-value" and initial_ticker:
            ticker = initial_ticker.upper().strip()
        elif triggered_id in ["ticker-search-button", "ticker-search-input"] and search_value:
            ticker = search_value.upper().strip()
        elif search_value:
            ticker = search_value.upper().strip()
        else:
            # No ticker to search
            return (
                html.P("Enter a ticker symbol above to search", className="text-muted"),
                None,
                hidden_style,
                hidden_style,
                hidden_style,
                hidden_style,
                "",
                empty_fig,
                None
            )
        
        # Look up ticker in database
        db = SessionLocal()
        try:
            stock = db.query(Stock).filter(Stock.ticker == ticker).first()
            
            if not stock:
                return (
                    dbc.Alert(
                        [
                            html.I(className="fas fa-exclamation-triangle me-2"),
                            f"Ticker '{ticker}' not found in the database. Please check the symbol and try again."
                        ],
                        color="warning",
                        className="mb-0"
                    ),
                    None,
                    hidden_style,
                    hidden_style,
                    hidden_style,
                    hidden_style,
                    "",
                    empty_fig,
                    None
                )
            
            # Get sub-industry info
            subindustry_code = stock.gics_subindustry_code
            subindustry_info = get_subindustry_info(db, subindustry_code)
            
            if not subindustry_info:
                return (
                    dbc.Alert(
                        f"Sub-industry information not found for {ticker}",
                        color="danger",
                        className="mb-0"
                    ),
                    None,
                    hidden_style,
                    hidden_style,
                    hidden_style,
                    hidden_style,
                    "",
                    empty_fig,
                    None
                )
            
            # Create success message with stock and sub-industry info
            result_message = dbc.Card([
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            html.H4([
                                html.I(className="fas fa-check-circle text-success me-2"),
                                f"{stock.ticker} - {stock.name}"
                            ], className="mb-0"),
                        ], md=6),
                        dbc.Col([
                            html.Div([
                                html.Span("Sub-Industry: ", className="text-muted"),
                                html.Strong(subindustry_info['name']),
                            ]),
                            html.Div([
                                html.Span("Sector: ", className="text-muted"),
                                html.Strong(subindustry_info['sector_name']),
                            ]),
                        ], md=6, className="text-md-end"),
                    ], className="align-items-center")
                ])
            ], className="bg-secondary border-success")
            
            # Get price data for the initial chart display
            price_df = get_stock_price_with_rs(db, ticker, num_weeks=52)
            
            # Create initial chart for the searched ticker
            chart_title = f"📊 {ticker} - {stock.name} | Daily Price & RS Indicator"
            
            if price_df.empty:
                chart_fig = go.Figure()
                chart_fig.update_layout(
                    title=f"No price data available for {ticker}",
                    paper_bgcolor=COLORS["paper_bg"],
                    plot_bgcolor=COLORS["plot_bg"],
                    font=dict(color=COLORS["text"]),
                )
            else:
                chart_fig = create_price_rs_chart(price_df, ticker, stock.name, "daily")
            
            # Store selected stock data
            stock_store_data = {
                "ticker": ticker,
                "stock_name": stock.name,
                "week_label": None,
                "percentile": None,
            }
            
            return (
                result_message,
                subindustry_code,
                visible_style,
                visible_style,
                visible_style,
                chart_visible_style,
                chart_title,
                chart_fig,
                stock_store_data
            )
            
        except Exception as e:
            logger.exception(f"Error searching ticker: {e}")
            return (
                dbc.Alert(f"Error: {str(e)}", color="danger", className="mb-0"),
                None,
                hidden_style,
                hidden_style,
                hidden_style,
                hidden_style,
                "",
                empty_fig,
                None
            )
        finally:
            db.close()
    
    @app.callback(
        Output("ticker-rs-heatmap", "figure"),
        Output("ticker-data-stats", "children"),
        Input("ticker-subindustry-code", "data"),
        Input("ticker-sort-method", "value"),
        Input("ticker-weeks-slider", "value"),
    )
    def update_ticker_heatmap(
        subindustry_code: Optional[str],
        sort_method: str,
        num_weeks: int
    ):
        """Generate and update the sub-industry heatmap for the found ticker."""
        
        if not subindustry_code:
            empty_fig = go.Figure()
            empty_fig.update_layout(
                paper_bgcolor=COLORS["paper_bg"],
                plot_bgcolor=COLORS["plot_bg"],
                font=dict(color=COLORS["text"]),
            )
            return empty_fig, ""
        
        db = SessionLocal()
        try:
            # Get sub-industry info for title
            subindustry_info = get_subindustry_info(db, subindustry_code)
            
            if not subindustry_info:
                empty_fig = go.Figure()
                empty_fig.update_layout(
                    title=f"Sub-industry {subindustry_code} not found",
                    paper_bgcolor=COLORS["paper_bg"],
                    plot_bgcolor=COLORS["plot_bg"],
                    font=dict(color=COLORS["text"]),
                )
                return empty_fig, ""
            
            # Get stock RS data
            df = get_stock_rs_matrix_data(
                db=db,
                subindustry_code=subindustry_code,
                num_weeks=num_weeks,
                sort_by=sort_method
            )
            
            # Stats
            stock_count = df['ticker'].nunique() if not df.empty else 0
            stats_text = f"{subindustry_info['name']} | Showing {stock_count} stocks | {num_weeks} weeks"
            
            if df.empty:
                empty_fig = go.Figure()
                empty_fig.update_layout(
                    title="No stock RS data available for this sub-industry",
                    paper_bgcolor=COLORS["paper_bg"],
                    plot_bgcolor=COLORS["plot_bg"],
                    font=dict(color=COLORS["text"]),
                )
                return empty_fig, stats_text
            
            # Create heatmap figure using the same function as stock page
            fig = create_stock_heatmap_figure(df, num_weeks)
            
            # Update title to show sub-industry name
            fig.update_layout(
                title=dict(
                    text=f"{subindustry_info['name']} Stocks<br><sup>← Most Recent | Weeks | Older →</sup>",
                )
            )
            
            return fig, stats_text
            
        except Exception as e:
            logger.exception(f"Error updating ticker heatmap: {e}")
            error_fig = go.Figure()
            error_fig.update_layout(
                title=f"Error loading data: {str(e)}",
                paper_bgcolor=COLORS["paper_bg"],
                font=dict(color="#ef4444"),
            )
            return error_fig, "Error loading data"
        finally:
            db.close()
    
    @app.callback(
        Output("ticker-detail-panel", "children"),
        Output("ticker-chart-container", "style", allow_duplicate=True),
        Output("ticker-price-rs-chart", "figure", allow_duplicate=True),
        Output("ticker-chart-title", "children", allow_duplicate=True),
        Output("ticker-selected-stock-store", "data", allow_duplicate=True),
        Input("ticker-rs-heatmap", "clickData"),
        Input("ticker-chart-timeframe-tabs", "active_tab"),
        State("ticker-selected-stock-store", "data"),
        prevent_initial_call=True
    )
    def show_ticker_detail_panel(click_data, timeframe, stored_stock):
        """Show price chart with RS indicator when any stock cell is clicked or timeframe changes."""
        
        # Styles
        hidden_style = {"display": "none"}
        visible_style = {"display": "block", "marginTop": "2.5rem", "paddingTop": "1rem"}
        
        # Empty figure for initial state
        empty_fig = go.Figure()
        empty_fig.update_layout(
            paper_bgcolor=COLORS["paper_bg"],
            plot_bgcolor=COLORS["plot_bg"],
            font=dict(color=COLORS["text"]),
        )
        
        # Default timeframe if not set
        if not timeframe:
            timeframe = "daily"
        
        # Determine what triggered the callback
        triggered_id = ctx.triggered_id if ctx.triggered_id else None
        
        # If tab changed, use stored stock info (if available)
        if triggered_id == "ticker-chart-timeframe-tabs" and stored_stock:
            ticker = stored_stock.get("ticker")
            stock_name = stored_stock.get("stock_name")
            week_label = stored_stock.get("week_label")
            percentile = stored_stock.get("percentile")
        elif click_data:
            # New cell click
            point = click_data['points'][0]
            ticker = point['y']  # Stock ticker on y-axis
            week_label = point['x']
            percentile = point.get('z')
            
            # Get stock name from database
            db = SessionLocal()
            try:
                stock = db.query(Stock).filter(Stock.ticker == ticker).first()
                stock_name = stock.name if stock else ticker
            finally:
                db.close()
        elif stored_stock:
            # Use stored stock for initial load
            ticker = stored_stock.get("ticker")
            stock_name = stored_stock.get("stock_name")
            week_label = stored_stock.get("week_label")
            percentile = stored_stock.get("percentile")
        else:
            # No click data and no stored stock
            return (
                html.P(
                    "Click any cell in the heatmap to see stock's price chart with RS indicator",
                    className="text-muted text-center mb-0"
                ),
                no_update,
                no_update,
                no_update,
                no_update
            )
        
        try:
            # Store the selected stock for tab switching
            stock_store_data = {
                "ticker": ticker,
                "stock_name": stock_name,
                "week_label": week_label,
                "percentile": percentile,
            }
            
            # Get price data from database
            db = SessionLocal()
            try:
                # Choose data based on timeframe
                if timeframe == "weekly":
                    price_df = get_stock_price_with_rs_weekly(db, ticker, num_weeks=104)
                else:
                    price_df = get_stock_price_with_rs(db, ticker, num_weeks=52)
            finally:
                db.close()
            
            # Chart title with timeframe indicator
            timeframe_label = "Weekly" if timeframe == "weekly" else "Daily"
            chart_title = f"📊 {ticker} - {stock_name} | {timeframe_label} Price & RS Indicator"
            
            # Show week and percentile info
            strength = get_strength_label(percentile) if percentile else "N/A"
            
            detail_content = []
            if week_label:
                detail_content = [
                    dbc.Row([
                        dbc.Col([
                            html.P([
                                html.Strong("Week: "),
                                week_label
                            ]),
                        ], md=4),
                        dbc.Col([
                            html.P([
                                html.Strong("RS Percentile: "),
                                f"{percentile:.0f}" if percentile else "N/A"
                            ]),
                        ], md=4),
                        dbc.Col([
                            html.P([
                                html.Strong("Strength: "),
                                strength
                            ]),
                        ], md=4),
                    ])
                ]
            
            detail_card = dbc.Card([
                dbc.CardHeader([
                    html.H5(f"📈 {ticker} - {stock_name}", className="mb-0")
                ]),
                dbc.CardBody(detail_content) if detail_content else None
            ], className="bg-secondary")
            
            # Create the price + RS chart
            if price_df.empty:
                error_fig = go.Figure()
                error_fig.update_layout(
                    title=f"No price data available for {ticker}",
                    paper_bgcolor=COLORS["paper_bg"],
                    plot_bgcolor=COLORS["plot_bg"],
                    font=dict(color=COLORS["text"]),
                )
                return detail_card, visible_style, error_fig, chart_title, stock_store_data
            
            fig = create_price_rs_chart(price_df, ticker, stock_name, timeframe)
            
            return detail_card, visible_style, fig, chart_title, stock_store_data
            
        except Exception as e:
            logger.exception(f"Error showing ticker detail panel: {e}")
            return (
                html.P(f"Error: {str(e)}", className="text-danger"),
                hidden_style,
                empty_fig,
                "",
                no_update
            )
