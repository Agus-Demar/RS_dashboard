"""
Stock drilldown page callbacks.

Handles:
- Stock-level RS heatmap generation
- TradingView chart display for individual stocks
- Page title updates
"""
import logging
from typing import Optional

import pandas as pd
import plotly.graph_objects as go
from dash import callback, Input, Output, State, html, no_update
import dash_bootstrap_components as dbc

from src.models import SessionLocal
from src.services.data_service import (
    get_stock_rs_matrix_data,
    get_subindustry_info,
)
from src.dashboard.utils.colors import get_color_scale, get_strength_label
from src.dashboard.utils.etf_mapper import get_tradingview_widget_url
from src.dashboard.utils.heatmap_config import (
    ROW_HEIGHT,
    STOCK_MARGINS,
    COLORS,
    FONT_SIZES,
)

logger = logging.getLogger(__name__)


def register_stock_callbacks(app):
    """Register all callbacks for the stock drilldown page."""
    
    @app.callback(
        Output("stock-rs-heatmap", "figure"),
        Output("stock-page-title", "children"),
        Output("stock-page-subtitle", "children"),
        Output("stock-data-stats", "children"),
        Output("stock-loading-overlay", "style"),
        Input("stock-subindustry-code", "data"),
        Input("stock-sort-method", "value"),
        Input("stock-weeks-slider", "value"),
    )
    def update_stock_heatmap(
        subindustry_code: Optional[str],
        sort_method: str,
        num_weeks: int
    ):
        """Generate and update the stock-level RS heatmap."""
        
        # Style to hide the loading overlay
        hide_overlay = {"display": "none"}
        
        if not subindustry_code:
            empty_fig = go.Figure()
            empty_fig.update_layout(
                title="No sub-industry selected",
                paper_bgcolor=COLORS["paper_bg"],
                plot_bgcolor=COLORS["plot_bg"],
                font=dict(color=COLORS["text"]),
            )
            return (
                empty_fig,
                "📈 Stock RS Heatmap",
                "Select a sub-industry from the main page",
                "",
                hide_overlay
            )
        
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
                return (
                    empty_fig,
                    "📈 Stock RS Heatmap",
                    "Sub-industry not found",
                    "",
                    hide_overlay
                )
            
            # Get stock RS data
            df = get_stock_rs_matrix_data(
                db=db,
                subindustry_code=subindustry_code,
                num_weeks=num_weeks,
                sort_by=sort_method
            )
            
            # Prepare title and subtitle
            title = f"📈 {subindustry_info['name']}"
            subtitle = f"{subindustry_info['sector_name']} | Click any cell to see TradingView chart"
            
            # Stats
            stock_count = df['ticker'].nunique() if not df.empty else 0
            stats_text = f"Showing {stock_count} stocks | {num_weeks} weeks"
            
            if df.empty:
                empty_fig = go.Figure()
                empty_fig.update_layout(
                    title="No stock RS data available for this sub-industry",
                    paper_bgcolor=COLORS["paper_bg"],
                    plot_bgcolor=COLORS["plot_bg"],
                    font=dict(color=COLORS["text"]),
                )
                return empty_fig, title, subtitle, stats_text, hide_overlay
            
            # Create heatmap figure
            fig = create_stock_heatmap_figure(df, num_weeks)
            
            return fig, title, subtitle, stats_text, hide_overlay
            
        except Exception as e:
            logger.exception(f"Error updating stock heatmap: {e}")
            error_fig = go.Figure()
            error_fig.update_layout(
                title=f"Error loading data: {str(e)}",
                paper_bgcolor=COLORS["paper_bg"],
                font=dict(color="#ef4444"),
            )
            return error_fig, "📈 Stock RS Heatmap", "Error", "Error loading data", hide_overlay
        finally:
            db.close()
    
    @app.callback(
        Output("stock-detail-panel", "children"),
        Output("stock-tradingview-container", "style"),
        Output("stock-tradingview-iframe", "src"),
        Output("stock-tradingview-title", "children"),
        Input("stock-rs-heatmap", "clickData"),
        State("stock-subindustry-code", "data"),
    )
    def show_stock_detail_panel(click_data, subindustry_code):
        """Show TradingView chart when any stock cell is clicked."""
        
        # Hidden style for TradingView container
        hidden_style = {"display": "none"}
        visible_style = {"display": "block", "marginTop": "2.5rem", "paddingTop": "1rem"}
        
        if not click_data:
            return (
                html.P(
                    "Click any cell to see stock's TradingView chart",
                    className="text-muted text-center mb-0"
                ),
                hidden_style,
                "",
                ""
            )
        
        try:
            point = click_data['points'][0]
            ticker = point['y']  # Stock ticker on y-axis
            week_label = point['x']
            percentile = point.get('z')
            
            # Get stock info from database
            db = SessionLocal()
            try:
                from src.models import Stock
                stock = db.query(Stock).filter(Stock.ticker == ticker).first()
                stock_name = stock.name if stock else ticker
            finally:
                db.close()
            
            # TradingView URL for the stock
            tradingview_url = get_tradingview_widget_url(ticker)
            tradingview_title = f"📊 {ticker} - {stock_name} | Weekly Chart"
            
            # Show week and percentile info
            strength = get_strength_label(percentile) if percentile else "N/A"
            
            detail_card = dbc.Card([
                dbc.CardHeader([
                    html.H5(f"📈 {ticker} - {stock_name}", className="mb-0")
                ]),
                dbc.CardBody([
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
                ])
            ], className="bg-secondary")
            
            return detail_card, visible_style, tradingview_url, tradingview_title
            
        except Exception as e:
            logger.exception(f"Error showing stock detail panel: {e}")
            return (
                html.P(f"Error: {str(e)}", className="text-danger"),
                hidden_style,
                "",
                ""
            )


def create_stock_heatmap_figure(df: pd.DataFrame, num_weeks: int) -> go.Figure:
    """
    Create the Plotly heatmap figure for individual stocks.
    
    Layout order (top to bottom):
    1. Main title
    2. Subtitle (week direction indicator)
    3. X-axis labels (top)
    4. Heatmap
    5. X-axis labels (bottom)
    
    Args:
        df: DataFrame with stock RS matrix data
        num_weeks: Number of weeks to display
    
    Returns:
        Plotly Figure object
    """
    from datetime import datetime
    
    # Pivot for heatmap: rows = stocks (ticker), columns = weeks
    pivot_df = df.pivot(
        index='ticker',
        columns='week_label',
        values='rs_percentile'
    )
    
    # Sort weeks: most recent FIRST (left side)
    week_order = sorted(pivot_df.columns, key=lambda x: datetime.strptime(x, "%d/%m/%y"), reverse=True)
    pivot_df = pivot_df[week_order]
    
    # Keep stock order from the sorted DataFrame
    unique_stocks = df.drop_duplicates('ticker')['ticker'].tolist()
    pivot_df = pivot_df.reindex(unique_stocks)
    
    # Create stock name map for hover text
    stock_names = df.drop_duplicates('ticker').set_index('ticker')['stock_name'].to_dict()
    
    # Build hover text matrix
    hover_text = []
    for ticker in pivot_df.index:
        row_text = []
        stock_name = stock_names.get(ticker, ticker)
        for week in pivot_df.columns:
            value = pivot_df.loc[ticker, week]
            if pd.isna(value):
                text = f"<b>{ticker}</b><br>{stock_name}<br>Week: {week}<br>No data"
            else:
                strength = get_strength_label(value)
                text = (
                    f"<b>{ticker}</b><br>"
                    f"{stock_name}<br>"
                    f"Week: {week}<br>"
                    f"RS Percentile: {value:.0f}<br>"
                    f"Strength: {strength}"
                )
            row_text.append(text)
        hover_text.append(row_text)
    
    # Create heatmap without colorbar
    fig = go.Figure(data=go.Heatmap(
        z=pivot_df.values,
        x=pivot_df.columns.tolist(),
        y=pivot_df.index.tolist(),
        colorscale=get_color_scale(),
        zmin=0,
        zmax=100,
        hovertemplate="%{customdata}<extra></extra>",
        customdata=hover_text,
        xgap=1,
        ygap=1,
        showscale=False,  # Hide colorbar
    ))
    
    # Add invisible scatter trace to enable top x-axis labels
    fig.add_trace(go.Scatter(
        x=pivot_df.columns.tolist(),
        y=[None] * len(pivot_df.columns),
        xaxis="x2",
        mode="markers",
        marker=dict(opacity=0),
        showlegend=False,
        hoverinfo="skip",
    ))
    
    # Calculate chart height with fixed row height of 32px
    num_stocks = len(pivot_df)
    fixed_row_height = 32
    # Increase top margin for title/subtitle visibility
    top_margin = 160
    bottom_margin = STOCK_MARGINS["bottom"]
    chart_height = num_stocks * fixed_row_height + top_margin + bottom_margin
    
    # Layout with title, subtitle, and dual x-axis (top and bottom)
    fig.update_layout(
        title=dict(
            text="Individual Stock Relative Strength<br><sup>← Most Recent | Weeks | Older →</sup>",
            font=dict(size=FONT_SIZES["subtitle"], color=COLORS["title"]),
            x=0.5,
            xanchor="center",
            y=0.88,  # Lowered to prevent cutoff
            yanchor="top",
        ),
        xaxis=dict(
            title=None,
            side="bottom",
            dtick=1,
            fixedrange=True,
            showticklabels=False,  # Hide bottom x-axis labels
        ),
        xaxis2=dict(
            title=None,
            tickfont=dict(size=FONT_SIZES["axis_label"], color=COLORS["muted_text"]),
            tickangle=-45,
            side="top",
            anchor="y",
            overlaying="x",
            fixedrange=True,
            showticklabels=True,
            tickmode="array",
            tickvals=pivot_df.columns.tolist(),
            ticktext=pivot_df.columns.tolist(),
            range=[-0.5, len(pivot_df.columns) - 0.5],
        ),
        yaxis=dict(
            title=None,
            tickfont=dict(size=FONT_SIZES["stock_axis_label"], color=COLORS["muted_text"]),
            autorange="reversed",
            tickmode="linear",
            dtick=1,
            fixedrange=True,
            ticklabelposition="outside",
        ),
        paper_bgcolor=COLORS["paper_bg"],
        plot_bgcolor=COLORS["plot_bg"],
        font=dict(color=COLORS["text"]),
        height=chart_height,
        margin=dict(
            l=STOCK_MARGINS["left"],
            r=STOCK_MARGINS["right"],
            t=top_margin,
            b=bottom_margin
        ),
    )
    
    # Add grid lines
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor=COLORS["grid"])
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor=COLORS["grid"])
    
    return fig
