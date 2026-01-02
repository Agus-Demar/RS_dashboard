"""
Heatmap callbacks for interactivity.

Handles:
- Heatmap generation and updates
- Sector filter population
- Cell click details
- Data statistics
"""
import logging
from typing import List, Optional

import pandas as pd
import plotly.graph_objects as go
from dash import callback, Input, Output, State, html, no_update
import dash_bootstrap_components as dbc

from src.models import SessionLocal
from src.services.data_service import (
    get_rs_matrix_data,
    get_available_sectors,
    get_subindustry_stocks,
    get_data_stats,
)
from src.dashboard.utils.colors import get_color_scale, get_strength_label

logger = logging.getLogger(__name__)


def register_callbacks(app):
    """Register all callbacks with the Dash app."""
    
    @app.callback(
        Output("rs-heatmap", "figure"),
        Output("sector-filter", "options"),
        Output("data-stats", "children"),
        Output("initial-loading-overlay", "style"),
        Input("sector-filter", "value"),
        Input("sort-method", "value"),
        Input("weeks-slider", "value"),
    )
    def update_heatmap(
        selected_sectors: Optional[List[str]],
        sort_method: str,
        num_weeks: int
    ):
        """Generate and update the RS heatmap."""
        
        db = SessionLocal()
        try:
            # Get RS data
            df = get_rs_matrix_data(
                db=db,
                num_weeks=num_weeks,
                sectors=selected_sectors,
                sort_by=sort_method
            )
            
            # Get available sectors for filter
            sectors = get_available_sectors(db)
            sector_options = [{"label": f"📁 {s}", "value": s} for s in sectors]
            
            # Get data statistics
            stats = get_data_stats(db)
            stats_text = (
                f"Data: {stats['stock_count']} stocks | "
                f"{stats['subindustry_count']} sub-industries | "
                f"{stats['rs_record_count']} RS records | "
                f"Latest: {stats['latest_rs_week'] or 'N/A'}"
            )
            
            # Style to hide the loading overlay
            hide_overlay = {"display": "none"}
            
            if df.empty:
                # Return empty figure
                empty_fig = go.Figure()
                empty_fig.update_layout(
                    title="No RS data available. Run the data pipeline first.",
                    paper_bgcolor="#0f172a",
                    plot_bgcolor="#1e293b",
                    font=dict(color="#e2e8f0"),
                )
                return empty_fig, sector_options, stats_text, hide_overlay
            
            # Create heatmap figure
            fig = create_heatmap_figure(df, num_weeks)
            
            return fig, sector_options, stats_text, hide_overlay
            
        except Exception as e:
            logger.exception(f"Error updating heatmap: {e}")
            error_fig = go.Figure()
            error_fig.update_layout(
                title=f"Error loading data: {str(e)}",
                paper_bgcolor="#0f172a",
                font=dict(color="#ef4444"),
            )
            return error_fig, [], "Error loading data", {"display": "none"}
        finally:
            db.close()
    
    @app.callback(
        Output("detail-panel", "children"),
        Input("rs-heatmap", "clickData"),
        State("rs-data-store", "data"),
    )
    def show_detail_panel(click_data, stored_data):
        """Show detailed information when a cell is clicked."""
        
        if not click_data:
            return html.P(
                "Click on a cell to see detailed RS information",
                className="text-muted text-center mb-0"
            )
        
        try:
            point = click_data['points'][0]
            subindustry_name = point['y']
            week_label = point['x']
            percentile = point['z']
            
            # Get stocks in this sub-industry
            db = SessionLocal()
            try:
                # We need to find the subindustry code from the name
                from src.models import GICSSubIndustry
                subindustry = db.query(GICSSubIndustry).filter(
                    GICSSubIndustry.name == subindustry_name
                ).first()
                
                if subindustry:
                    stocks = get_subindustry_stocks(db, subindustry.code)
                else:
                    stocks = []
            finally:
                db.close()
            
            # Format stocks list
            if stocks:
                stock_items = [
                    html.Li(
                        f"{s['ticker']} - {s['name'][:40]}..."
                        if len(s['name']) > 40 else f"{s['ticker']} - {s['name']}",
                        className="small"
                    )
                    for s in stocks[:10]  # Top 10 by market cap
                ]
                if len(stocks) > 10:
                    stock_items.append(
                        html.Li(f"... and {len(stocks) - 10} more", className="small text-muted")
                    )
                stocks_section = html.Ul(stock_items, className="mb-0")
            else:
                stocks_section = html.P("No stocks found", className="text-muted small")
            
            strength = get_strength_label(percentile) if percentile else "N/A"
            
            return dbc.Card([
                dbc.CardHeader([
                    html.H5(f"📈 {subindustry_name}", className="mb-0")
                ]),
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            html.P([
                                html.Strong("Week: "),
                                week_label
                            ]),
                            html.P([
                                html.Strong("RS Percentile: "),
                                f"{percentile:.0f}" if percentile else "N/A"
                            ]),
                            html.P([
                                html.Strong("Strength: "),
                                strength
                            ]),
                        ], md=4),
                        dbc.Col([
                            html.P(html.Strong("Top Stocks (by Market Cap):")),
                            stocks_section
                        ], md=8),
                    ])
                ])
            ], className="bg-secondary")
            
        except Exception as e:
            logger.exception(f"Error showing detail panel: {e}")
            return html.P(f"Error: {str(e)}", className="text-danger")


def create_heatmap_figure(df: pd.DataFrame, num_weeks: int) -> go.Figure:
    """
    Create the Plotly heatmap figure.
    
    Args:
        df: DataFrame with RS matrix data
        num_weeks: Number of weeks to display
    
    Returns:
        Plotly Figure object
    """
    # Pivot for heatmap: rows = sub-industries, columns = weeks
    pivot_df = df.pivot(
        index='subindustry_name',   # Y-axis
        columns='week_label',        # X-axis
        values='rs_percentile'
    )
    
    # Sort weeks: most recent FIRST (left side)
    week_order = sorted(pivot_df.columns, key=lambda x: int(x.split('-')[1]))
    pivot_df = pivot_df[week_order]
    
    # Keep sub-industry order from the sorted DataFrame
    unique_subindustries = df.drop_duplicates('subindustry_name')['subindustry_name'].tolist()
    pivot_df = pivot_df.reindex(unique_subindustries)
    
    # Build hover text matrix
    hover_text = []
    for industry in pivot_df.index:
        row_text = []
        for week in pivot_df.columns:
            value = pivot_df.loc[industry, week]
            if pd.isna(value):
                text = f"<b>{industry}</b><br>Week: {week}<br>No data"
            else:
                strength = get_strength_label(value)
                text = (
                    f"<b>{industry}</b><br>"
                    f"Week: {week}<br>"
                    f"RS Percentile: {value:.0f}<br>"
                    f"Strength: {strength}"
                )
            row_text.append(text)
        hover_text.append(row_text)
    
    # Create heatmap
    fig = go.Figure(data=go.Heatmap(
        z=pivot_df.values,
        x=pivot_df.columns.tolist(),     # Weeks on X-axis
        y=pivot_df.index.tolist(),        # Sub-industries on Y-axis
        colorscale=get_color_scale(),
        zmin=0,
        zmax=100,
        hovertemplate="%{customdata}<extra></extra>",
        customdata=hover_text,
        xgap=1,  # Gap between cells
        ygap=1,
        colorbar=dict(
            title=dict(text="RS Percentile", side="right"),
            tickvals=[0, 25, 50, 75, 100],
            ticktext=["0 (Weak)", "25", "50", "75", "100 (Strong)"],
            len=0.75,
        )
    ))
    
    # Layout configuration
    num_industries = len(pivot_df)
    
    fig.update_layout(
        title=dict(
            text="📊 Mansfield Relative Strength by GICS Sub-Industry",
            font=dict(size=20, color="#f8fafc"),
            x=0.5,
            xanchor="center"
        ),
        xaxis=dict(
            title=dict(text="← Most Recent | Weeks | Older →", font=dict(size=12)),
            tickfont=dict(size=10, color="#94a3b8"),
            tickangle=0,
            side="top",
            dtick=1,
        ),
        yaxis=dict(
            title=dict(text="GICS Sub-Industries", font=dict(size=12)),
            tickfont=dict(size=9, color="#94a3b8"),
            autorange="reversed",  # First industry at top
            tickmode="linear",
            dtick=1,
        ),
        paper_bgcolor="#0f172a",   # Slate 900
        plot_bgcolor="#1e293b",    # Slate 800
        font=dict(color="#e2e8f0"),
        height=max(600, num_industries * 18 + 150),
        margin=dict(l=280, r=80, t=100, b=50),
    )
    
    # Add grid lines
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor="#334155")
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor="#334155")
    
    return fig

