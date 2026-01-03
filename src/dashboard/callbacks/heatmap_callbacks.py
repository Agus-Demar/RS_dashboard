"""
Heatmap callbacks for interactivity.

Handles:
- Heatmap generation and updates
- Sector filter population
- Cell click navigation to stock drilldown
- Chart column for TradingView (on right side)
"""
import logging
from typing import List, Optional

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from dash import callback, Input, Output, State, html, no_update, dcc
import dash_bootstrap_components as dbc

from src.models import SessionLocal
from src.services.data_service import (
    get_rs_matrix_data,
    get_available_sectors,
    get_subindustry_stocks,
    get_data_stats,
)
from src.dashboard.utils.colors import get_color_scale, get_strength_label
from src.dashboard.utils.etf_mapper import get_etf_for_subindustry, get_tradingview_widget_url
from src.dashboard.utils.heatmap_config import (
    CHART_COLUMN,
    ROW_HEIGHT,
    MAX_LABEL_LENGTH,
    MARGINS,
    MIN_MAIN_CHART_HEIGHT,
    COLORS,
    FONT_SIZES,
)

logger = logging.getLogger(__name__)


def register_callbacks(app):
    """Register all callbacks with the Dash app."""
    
    @app.callback(
        Output("rs-heatmap", "figure"),
        Output("sector-filter", "options"),
        Output("data-stats", "children"),
        Output("initial-loading-overlay", "style"),
        Output("rs-data-store", "data"),
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
                    paper_bgcolor=COLORS["paper_bg"],
                    plot_bgcolor=COLORS["plot_bg"],
                    font=dict(color=COLORS["text"]),
                )
                return empty_fig, sector_options, stats_text, hide_overlay, None
            
            # Store subindustry name to code mapping for navigation
            subindustry_map = df[['subindustry_name', 'subindustry_code']].drop_duplicates()
            name_to_code = dict(zip(subindustry_map['subindustry_name'], subindustry_map['subindustry_code']))
            
            # Create heatmap figure with chart column on right
            fig = create_heatmap_figure(df, num_weeks)
            
            return fig, sector_options, stats_text, hide_overlay, name_to_code
            
        except Exception as e:
            logger.exception(f"Error updating heatmap: {e}")
            error_fig = go.Figure()
            error_fig.update_layout(
                title=f"Error loading data: {str(e)}",
                paper_bgcolor=COLORS["paper_bg"],
                font=dict(color="#ef4444"),
            )
            return error_fig, [], "Error loading data", {"display": "none"}, None
        finally:
            db.close()
    
    @app.callback(
        Output("detail-panel", "children"),
        Output("tradingview-container", "style"),
        Output("tradingview-iframe", "src"),
        Output("tradingview-title", "children"),
        Output("url", "pathname"),
        Input("rs-heatmap", "clickData"),
        State("rs-data-store", "data"),
    )
    def handle_heatmap_click(click_data, name_to_code):
        """Handle heatmap clicks - chart column shows TradingView, data cells navigate to stocks."""
        
        # Hidden style for TradingView container
        hidden_style = {"display": "none"}
        visible_style = {"display": "block", "marginTop": "2.5rem", "paddingTop": "1rem"}
        
        if not click_data:
            return (
                html.P(
                    "Click 📈 icon (right side) for sector ETF chart | Click data cell to drill down to stocks",
                    className="text-muted text-center mb-0"
                ),
                hidden_style,
                "",
                "",
                no_update  # Don't navigate
            )
        
        try:
            point = click_data['points'][0]
            subindustry_name = point['y']
            week_label = point['x']
            percentile = point.get('z')
            
            # Check if clicking on the chart column (now on right side)
            if week_label == CHART_COLUMN:
                # Show TradingView chart for sub-industry ETF
                return show_tradingview_for_subindustry(subindustry_name)
            
            # Otherwise, navigate to stock drilldown page
            if name_to_code and subindustry_name in name_to_code:
                subindustry_code = name_to_code[subindustry_name]
                # Navigate to stock page
                return (
                    html.P(
                        f"Navigating to {subindustry_name}...",
                        className="text-info text-center mb-0"
                    ),
                    hidden_style,
                    "",
                    "",
                    f"/stocks/{subindustry_code}"  # Navigate to stock drilldown
                )
            
            # Fallback: show detail panel without navigation
            return show_detail_panel_content(subindustry_name, week_label, percentile)
            
        except Exception as e:
            logger.exception(f"Error handling heatmap click: {e}")
            return (
                html.P(f"Error: {str(e)}", className="text-danger"),
                hidden_style,
                "",
                "",
                no_update
            )


def show_tradingview_for_subindustry(subindustry_name: str):
    """Show TradingView chart for sub-industry ETF."""
    hidden_style = {"display": "none"}
    visible_style = {"display": "block", "marginTop": "2.5rem", "paddingTop": "1rem"}
    
    db = SessionLocal()
    try:
        from src.models import GICSSubIndustry
        subindustry = db.query(GICSSubIndustry).filter(
            GICSSubIndustry.name == subindustry_name
        ).first()
        
        if subindustry:
            stocks = get_subindustry_stocks(db, subindustry.code)
            sector_name = subindustry.sector_name
        else:
            stocks = []
            sector_name = None
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
            for s in stocks[:10]
        ]
        if len(stocks) > 10:
            stock_items.append(
                html.Li(f"... and {len(stocks) - 10} more", className="small text-muted")
            )
        stocks_section = html.Ul(stock_items, className="mb-0")
    else:
        stocks_section = html.P("No stocks found", className="text-muted small")
    
    # Get ETF for TradingView widget
    etf_symbol = get_etf_for_subindustry(subindustry_name, sector_name or "")
    tradingview_url = get_tradingview_widget_url(etf_symbol)
    tradingview_title = f"📊 {etf_symbol} - Weekly Chart ({sector_name or 'Sector'} ETF)"
    
    detail_card = dbc.Card([
        dbc.CardHeader([
            html.H5(f"📈 {subindustry_name}", className="mb-0")
        ]),
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    html.P([
                        html.Strong("Sector ETF: "),
                        etf_symbol
                    ]),
                    html.P(
                        "Click on a data cell to drill down to individual stocks",
                        className="text-muted small"
                    ),
                ], md=4),
                dbc.Col([
                    html.P(html.Strong("Top Stocks (by Market Cap):")),
                    stocks_section
                ], md=8),
            ])
        ])
    ], className="bg-secondary")
    
    return detail_card, visible_style, tradingview_url, tradingview_title, no_update


def show_detail_panel_content(subindustry_name: str, week_label: str, percentile):
    """Show detail panel without navigation (fallback)."""
    hidden_style = {"display": "none"}
    visible_style = {"display": "block", "marginTop": "2.5rem", "paddingTop": "1rem"}
    
    db = SessionLocal()
    try:
        from src.models import GICSSubIndustry
        subindustry = db.query(GICSSubIndustry).filter(
            GICSSubIndustry.name == subindustry_name
        ).first()
        
        if subindustry:
            stocks = get_subindustry_stocks(db, subindustry.code)
            sector_name = subindustry.sector_name
        else:
            stocks = []
            sector_name = None
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
            for s in stocks[:10]
        ]
        if len(stocks) > 10:
            stock_items.append(
                html.Li(f"... and {len(stocks) - 10} more", className="small text-muted")
            )
        stocks_section = html.Ul(stock_items, className="mb-0")
    else:
        stocks_section = html.P("No stocks found", className="text-muted small")
    
    strength = get_strength_label(percentile) if percentile else "N/A"
    
    # Get ETF for TradingView widget
    etf_symbol = get_etf_for_subindustry(subindustry_name, sector_name or "")
    tradingview_url = get_tradingview_widget_url(etf_symbol)
    tradingview_title = f"📊 {etf_symbol} - Weekly Chart ({sector_name or 'Sector'} ETF)"
    
    detail_card = dbc.Card([
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
                    html.P([
                        html.Strong("Sector ETF: "),
                        etf_symbol
                    ]),
                ], md=4),
                dbc.Col([
                    html.P(html.Strong("Top Stocks (by Market Cap):")),
                    stocks_section
                ], md=8),
            ])
        ])
    ], className="bg-secondary")
    
    return detail_card, visible_style, tradingview_url, tradingview_title, no_update


def create_heatmap_figure(df: pd.DataFrame, num_weeks: int) -> go.Figure:
    """
    Create the Plotly heatmap figure with chart column on right side.
    
    Layout order (top to bottom):
    1. Main title
    2. Week legend annotation
    3. Heatmap with x-axis labels on bottom
    
    Args:
        df: DataFrame with RS matrix data
        num_weeks: Number of weeks to display
    
    Returns:
        Plotly Figure object
    """
    from datetime import datetime
    
    # Pivot for heatmap: rows = sub-industries, columns = weeks
    pivot_df = df.pivot(
        index='subindustry_name',
        columns='week_label',
        values='rs_percentile'
    )
    
    # Sort weeks: most recent FIRST (left side)
    week_order = sorted(pivot_df.columns, key=lambda x: datetime.strptime(x, "%d/%m/%y"), reverse=True)
    pivot_df = pivot_df[week_order]
    
    # Keep sub-industry order from the sorted DataFrame
    unique_subindustries = df.drop_duplicates('subindustry_name')['subindustry_name'].tolist()
    pivot_df = pivot_df.reindex(unique_subindustries)
    
    # Add chart column on the RIGHT side with NaN values (renders as background color)
    chart_col_values = [np.nan] * len(pivot_df)
    pivot_df[CHART_COLUMN] = chart_col_values
    
    # Column order: weeks first, then chart column on right
    columns_order = week_order + [CHART_COLUMN]
    pivot_df = pivot_df[columns_order]
    
    # Build hover text matrix
    hover_text = []
    for industry in pivot_df.index:
        row_text = []
        for week in pivot_df.columns:
            if week == CHART_COLUMN:
                text = f"<b>📈 View ETF Chart</b><br>{industry}<br>Click to show TradingView"
            else:
                value = pivot_df.loc[industry, week]
                if pd.isna(value):
                    text = f"<b>{industry}</b><br>Week: {week}<br>No data<br><i>Click to view stocks</i>"
                else:
                    strength = get_strength_label(value)
                    text = (
                        f"<b>{industry}</b><br>"
                        f"Week: {week}<br>"
                        f"RS Percentile: {value:.0f}<br>"
                        f"Strength: {strength}<br>"
                        f"<i>Click to view stocks</i>"
                    )
            row_text.append(text)
        hover_text.append(row_text)
    
    # Create heatmap
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
        colorbar=dict(
            title=dict(text="RS Percentile", side="right"),
            tickvals=[0, 25, 50, 75, 100],
            ticktext=["0 (Weak)", "25", "50", "75", "100 (Strong)"],
            len=0.75,
        )
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
    
    # Calculate chart height based on row count
    num_industries = len(pivot_df)
    chart_height = max(MIN_MAIN_CHART_HEIGHT, num_industries * ROW_HEIGHT + MARGINS["top"] + MARGINS["bottom"])
    
    # Truncate long sub-industry names
    y_labels = [
        (name[:MAX_LABEL_LENGTH] + "...") if len(name) > MAX_LABEL_LENGTH else name
        for name in pivot_df.index.tolist()
    ]
    
    # Build annotations for chart icons in each row
    chart_annotations = []
    for industry in pivot_df.index:
        chart_annotations.append(
            dict(
                text="📈",
                x=CHART_COLUMN,
                y=industry,
                xref="x",
                yref="y",
                showarrow=False,
                font=dict(size=FONT_SIZES["chart_icon"], color=COLORS["text"]),
            )
        )
    
    # Layout with title, subtitle, and dual x-axis (top and bottom)
    fig.update_layout(
        title=dict(
            text="📊 Mansfield Relative Strength by GICS Sub-Industry<br><sup>← Most Recent | Weeks | Older → | 📈 = ETF Chart</sup>",
            font=dict(size=FONT_SIZES["title"], color=COLORS["title"]),
            x=0.5,
            xanchor="center",
            y=0.99,
            yanchor="top",
        ),
        xaxis=dict(
            title=None,
            tickfont=dict(size=FONT_SIZES["axis_label"], color=COLORS["muted_text"]),
            tickangle=45,
            side="bottom",
            dtick=1,
            fixedrange=True,
            showticklabels=True,
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
            tickfont=dict(size=FONT_SIZES["axis_label"], color=COLORS["muted_text"]),
            autorange="reversed",
            tickmode="linear",
            dtick=1,
            fixedrange=True,
            ticklabelposition="outside",
        ),
        annotations=chart_annotations,
        paper_bgcolor=COLORS["paper_bg"],
        plot_bgcolor=COLORS["plot_bg"],
        font=dict(color=COLORS["text"]),
        height=chart_height,
        margin=dict(
            l=MARGINS["left"],
            r=MARGINS["right"],
            t=MARGINS["top"],
            b=MARGINS["bottom"]
        ),
    )
    
    # Update y-axis with truncated labels
    fig.update_yaxes(
        ticktext=y_labels,
        tickvals=pivot_df.index.tolist(),
    )
    
    # Add grid lines
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor=COLORS["grid"])
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor=COLORS["grid"])
    
    return fig
