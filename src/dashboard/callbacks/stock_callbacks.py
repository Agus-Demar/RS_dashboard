"""
Stock drilldown page callbacks.

Handles:
- Stock-level RS heatmap generation
- Price chart with RS indicator display for individual stocks
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
    get_stock_sctr_matrix_data,
    get_subindustry_info,
    get_stock_price_with_rs,
    get_stock_price_with_rs_weekly,
)
from plotly.subplots import make_subplots

from src.dashboard.utils.colors import get_color_scale, get_strength_label
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
        Output("stock-color-legend", "children"),
        Input("stock-subindustry-code", "data"),
        Input("stock-sort-method", "value"),
        Input("stock-weeks-slider", "value"),
        Input("stock-metric-tabs", "active_tab"),
    )
    def update_stock_heatmap(
        subindustry_code: Optional[str],
        sort_method: str,
        num_weeks: int,
        active_tab: str
    ):
        """Generate and update the stock-level RS or SCTR heatmap based on active tab."""
        
        # Determine if we're showing RS or SCTR
        is_sctr = active_tab == "sctr"
        metric_name = "SCTR" if is_sctr else "RS"
        
        # Set legend based on active tab
        if is_sctr:
            legend = [
                html.Span("🔴 Lagging (0-40)", className="mx-3"),
                html.Span("🟡 Neutral (40-60)", className="mx-3"),
                html.Span("🟢 Leading (60-100)", className="mx-3"),
            ]
        else:
            legend = [
                html.Span("🔴 Weak (Bottom 33%)", className="mx-3"),
                html.Span("🟡 Neutral (Middle 34%)", className="mx-3"),
                html.Span("🟢 Strong (Top 33%)", className="mx-3"),
            ]
        
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
                f"📈 Stock {metric_name} Heatmap",
                "Select a sub-industry from the main page",
                "",
                hide_overlay,
                legend
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
                    f"📈 Stock {metric_name} Heatmap",
                    "Sub-industry not found",
                    "",
                    hide_overlay,
                    legend
                )
            
            # Get stock data based on active tab
            if is_sctr:
                df = get_stock_sctr_matrix_data(
                    db=db,
                    subindustry_code=subindustry_code,
                    num_weeks=num_weeks,
                    sort_by=sort_method
                )
            else:
                df = get_stock_rs_matrix_data(
                    db=db,
                    subindustry_code=subindustry_code,
                    num_weeks=num_weeks,
                    sort_by=sort_method
                )
            
            # Prepare title and subtitle
            title = f"📈 {subindustry_info['name']}"
            if is_sctr:
                subtitle = f"{subindustry_info['sector_name']} | SCTR Analysis | Click any cell to see price chart"
            else:
                subtitle = f"{subindustry_info['sector_name']} | Click any cell to see price chart with RS indicator"
            
            # Stats
            stock_count = df['ticker'].nunique() if not df.empty else 0
            stats_text = f"Showing {stock_count} stocks | {num_weeks} weeks | {metric_name} ranking"
            
            if df.empty:
                empty_fig = go.Figure()
                empty_fig.update_layout(
                    title=f"No stock {metric_name} data available for this sub-industry",
                    paper_bgcolor=COLORS["paper_bg"],
                    plot_bgcolor=COLORS["plot_bg"],
                    font=dict(color=COLORS["text"]),
                )
                return empty_fig, title, subtitle, stats_text, hide_overlay, legend
            
            # Create heatmap figure
            if is_sctr:
                fig = create_stock_sctr_heatmap_figure(df, num_weeks)
            else:
                fig = create_stock_heatmap_figure(df, num_weeks)
            
            return fig, title, subtitle, stats_text, hide_overlay, legend
            
        except Exception as e:
            logger.exception(f"Error updating stock heatmap: {e}")
            error_fig = go.Figure()
            error_fig.update_layout(
                title=f"Error loading data: {str(e)}",
                paper_bgcolor=COLORS["paper_bg"],
                font=dict(color="#ef4444"),
            )
            return error_fig, f"📈 Stock {metric_name} Heatmap", "Error", "Error loading data", hide_overlay, legend
        finally:
            db.close()
    
    @app.callback(
        Output("stock-detail-panel", "children"),
        Output("stock-chart-container", "style"),
        Output("stock-price-rs-chart", "figure"),
        Output("stock-chart-title", "children"),
        Output("selected-stock-store", "data"),
        Input("stock-rs-heatmap", "clickData"),
        Input("chart-timeframe-tabs", "active_tab"),
        State("stock-subindustry-code", "data"),
        State("selected-stock-store", "data"),
    )
    def show_stock_detail_panel(click_data, timeframe, subindustry_code, stored_stock):
        """Show price chart with RS indicator when any stock cell is clicked or timeframe changes."""
        from dash import ctx
        
        # Hidden style for chart container
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
        if triggered_id == "chart-timeframe-tabs" and stored_stock:
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
                from src.models import Stock
                stock = db.query(Stock).filter(Stock.ticker == ticker).first()
                stock_name = stock.name if stock else ticker
            finally:
                db.close()
        else:
            # No click data and no stored stock
            return (
                html.P(
                    "Click any cell to see stock's price chart with RS indicator",
                    className="text-muted text-center mb-0"
                ),
                hidden_style,
                empty_fig,
                "",
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
            logger.exception(f"Error showing stock detail panel: {e}")
            return (
                html.P(f"Error: {str(e)}", className="text-danger"),
                hidden_style,
                empty_fig,
                "",
                no_update
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


def create_stock_sctr_heatmap_figure(df: pd.DataFrame, num_weeks: int) -> go.Figure:
    """
    Create the Plotly SCTR heatmap figure for individual stocks.
    
    Args:
        df: DataFrame with stock SCTR matrix data
        num_weeks: Number of weeks to display
    
    Returns:
        Plotly Figure object
    """
    from datetime import datetime
    
    # Pivot for heatmap: rows = stocks (ticker), columns = weeks
    pivot_df = df.pivot(
        index='ticker',
        columns='week_label',
        values='sctr_percentile'
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
                strength = get_sctr_strength_label(value)
                text = (
                    f"<b>{ticker}</b><br>"
                    f"{stock_name}<br>"
                    f"Week: {week}<br>"
                    f"SCTR Percentile: {value:.0f}<br>"
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
            text="Individual Stock Technical Rank (SCTR)<br><sup>← Most Recent | Weeks | Older →</sup>",
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


def get_sctr_strength_label(percentile: float) -> str:
    """
    Get SCTR strength label based on percentile.
    
    SCTR interpretation:
    - 60-100: Leading (strong technical strength)
    - 40-60: Neutral
    - 0-40: Lagging (weak technical strength)
    
    Args:
        percentile: SCTR percentile value (0-100)
    
    Returns:
        Strength label string
    """
    if percentile is None:
        return "N/A"
    if percentile >= 60:
        return "Leading"
    elif percentile >= 40:
        return "Neutral"
    else:
        return "Lagging"


def create_price_rs_chart(df: pd.DataFrame, ticker: str, stock_name: str, timeframe: str = "daily") -> go.Figure:
    """
    Create a Plotly figure with candlestick price chart, RS indicator, and Cardwell RSI subplots.
    
    Based on Pine Script indicators:
    - RS Line = Close / Benchmark Close (white line)
    - RS EMA 13 = 13-period EMA (gray line)
    - RS EMA 52 = 52-period EMA (purple line)
    - Cardwell RSI with zones
    
    Args:
        df: DataFrame with OHLC data, RS calculations, and RSI data
        ticker: Stock ticker symbol
        stock_name: Stock company name
        timeframe: "daily" or "weekly" - affects title and rangebreaks
    
    Returns:
        Plotly Figure with four subplots
    """
    from plotly.subplots import make_subplots
    
    # Filter out rows with null values in critical OHLC columns
    df = df.dropna(subset=['open', 'high', 'low', 'close']).copy()
    
    if df.empty:
        empty_fig = go.Figure()
        empty_fig.update_layout(
            title=f"No valid price data for {ticker}",
            paper_bgcolor=COLORS["paper_bg"],
            plot_bgcolor=COLORS["plot_bg"],
            font=dict(color=COLORS["text"]),
        )
        return empty_fig
    
    # Build list of date gaps (holidays, etc.) to exclude from chart
    # This prevents gaps in the chart for non-trading days
    all_dates = pd.date_range(start=df['date'].min(), end=df['date'].max(), freq='D')
    trading_dates = set(df['date'].dt.date if hasattr(df['date'].iloc[0], 'date') else df['date'])
    
    # Convert to set of date objects for comparison
    if hasattr(df['date'].iloc[0], 'date'):
        trading_dates = set(d.date() for d in df['date'])
    else:
        trading_dates = set(df['date'])
    
    # Find gaps (non-trading days that aren't weekends)
    date_gaps = []
    for d in all_dates:
        if d.weekday() < 5 and d.date() not in trading_dates:  # Weekday but not in data
            date_gaps.append(d)
    
    # Create figure with four subplots (Price, Volume, RS, RSI)
    fig = make_subplots(
        rows=4, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.03,
        row_heights=[0.40, 0.12, 0.24, 0.24],
        subplot_titles=(
            f"{ticker} - Price",
            "Volume",
            "Relative Strength (RS) vs SPY",
            "Cardwell RSI"
        )
    )
    
    # ===================
    # Row 1: Candlestick price chart with EMAs
    # ===================
    fig.add_trace(
        go.Candlestick(
            x=df['date'],
            open=df['open'],
            high=df['high'],
            low=df['low'],
            close=df['close'],
            name='Price',
            increasing=dict(line=dict(color='#22c55e'), fillcolor='#22c55e'),  # Green
            decreasing=dict(line=dict(color='#ef4444'), fillcolor='#ef4444'),  # Red
        ),
        row=1, col=1
    )
    
    # 10-week EMA (light grey) - short-term trend
    if 'ema_10' in df.columns:
        fig.add_trace(
            go.Scatter(
                x=df['date'],
                y=df['ema_10'],
                mode='lines',
                name='EMA 10',
                line=dict(color='#9ca3af', width=1),  # Light grey, thin
                hovertemplate='EMA 10: $%{y:.2f}<extra></extra>'
            ),
            row=1, col=1
        )
    
    # 30-week EMA (orange) - medium-term trend (Weinstein method)
    if 'ema_30' in df.columns:
        fig.add_trace(
            go.Scatter(
                x=df['date'],
                y=df['ema_30'],
                mode='lines',
                name='EMA 30',
                line=dict(color='#f97316', width=1.5),  # Orange, slightly thinner
                hovertemplate='EMA 30: $%{y:.2f}<extra></extra>'
            ),
            row=1, col=1
        )
    
    # ===================
    # Row 2: Volume
    # ===================
    
    # Calculate volume bar colors based on price direction
    colors = ['#22c55e' if close >= open_price else '#ef4444' 
              for close, open_price in zip(df['close'], df['open'])]
    
    fig.add_trace(
        go.Bar(
            x=df['date'],
            y=df['volume'],
            name='Volume',
            marker=dict(color=colors, opacity=0.7),
            hovertemplate='Volume: %{y:,.0f}<extra></extra>'
        ),
        row=2, col=1
    )
    
    # ===================
    # Row 3: RS indicator
    # ===================
    
    # RS Line (white) - main RS indicator
    fig.add_trace(
        go.Scatter(
            x=df['date'],
            y=df['rs_line'],
            mode='lines',
            name='RS Line',
            line=dict(color='#ffffff', width=1.5),
            hovertemplate='RS: %{y:.4f}<extra></extra>'
        ),
        row=3, col=1
    )
    
    # RS EMA 13 (gray) - short-term average
    fig.add_trace(
        go.Scatter(
            x=df['date'],
            y=df['rs_ema_13'],
            mode='lines',
            name='RS EMA 13',
            line=dict(color='#9ca3af', width=1, dash='dot'),
            hovertemplate='EMA 13: %{y:.4f}<extra></extra>'
        ),
        row=3, col=1
    )
    
    # RS EMA 52 (purple) - long-term average
    fig.add_trace(
        go.Scatter(
            x=df['date'],
            y=df['rs_ema_52'],
            mode='lines',
            name='RS EMA 52',
            line=dict(color='#a855f7', width=1.5),
            hovertemplate='EMA 52: %{y:.4f}<extra></extra>'
        ),
        row=3, col=1
    )
    
    # ===================
    # Row 4: Cardwell RSI
    # ===================
    
    # Bull zone fill (80-40) - green background
    fig.add_trace(
        go.Scatter(
            x=list(df['date']) + list(df['date'][::-1]),
            y=[80] * len(df) + [40] * len(df),
            fill='toself',
            fillcolor='rgba(34, 197, 94, 0.08)',  # Green with 8% opacity
            line=dict(width=0),
            showlegend=False,
            hoverinfo='skip',
        ),
        row=4, col=1
    )
    
    # Bear zone fill (60-20) - orange background
    fig.add_trace(
        go.Scatter(
            x=list(df['date']) + list(df['date'][::-1]),
            y=[60] * len(df) + [20] * len(df),
            fill='toself',
            fillcolor='rgba(255, 106, 0, 0.08)',  # Orange with 8% opacity
            line=dict(width=0),
            showlegend=False,
            hoverinfo='skip',
        ),
        row=4, col=1
    )
    
    # RSI 14 (white) - main RSI line
    fig.add_trace(
        go.Scatter(
            x=df['date'],
            y=df['rsi_14'],
            mode='lines',
            name='RSI 14',
            line=dict(color='#ffffff', width=1.5),
            hovertemplate='RSI: %{y:.1f}<extra></extra>'
        ),
        row=4, col=1
    )
    
    # RSI SMA 9 (blue)
    fig.add_trace(
        go.Scatter(
            x=df['date'],
            y=df['rsi_sma_9'],
            mode='lines',
            name='RSI SMA 9',
            line=dict(color='#3b82f6', width=1),
            hovertemplate='SMA 9: %{y:.1f}<extra></extra>'
        ),
        row=4, col=1
    )
    
    # RSI EMA 45 (orange)
    fig.add_trace(
        go.Scatter(
            x=df['date'],
            y=df['rsi_ema_45'],
            mode='lines',
            name='RSI EMA 45',
            line=dict(color='#FF6A00', width=1.5),
            hovertemplate='EMA 45: %{y:.1f}<extra></extra>'
        ),
        row=4, col=1
    )
    
    # ===================
    # Layout styling
    # ===================
    # Timeframe label for title
    timeframe_label = "Weekly" if timeframe == "weekly" else "Daily"
    
    fig.update_layout(
        title=dict(
            text=f"{ticker} - {stock_name}<br><sup>{timeframe_label} Price Chart with RS & Cardwell RSI Indicators</sup>",
            font=dict(size=16, color=COLORS["title"]),
            x=0.5,
            xanchor="center",
            y=0.98,
            yanchor="top",
        ),
        paper_bgcolor=COLORS["paper_bg"],
        plot_bgcolor=COLORS["plot_bg"],
        font=dict(color=COLORS["text"]),
        height=1000,  # Increased height for 4 subplots
        margin=dict(l=60, r=40, t=120, b=40),  # Increased top margin for title/legend spacing
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="top",
            y=1.12,  # Moved higher to avoid overlap with title
            xanchor="center",
            x=0.5,
            bgcolor="rgba(0,0,0,0)",
            font=dict(size=9, color=COLORS["muted_text"]),
        ),
        xaxis_rangeslider_visible=False,
        hovermode='x unified',
    )
    
    # Build rangebreaks for weekends and holidays/gaps (only for daily charts)
    rangebreaks_list = []
    if timeframe == "daily":
        rangebreaks_list.append(dict(bounds=["sat", "mon"]))  # Hide Saturday and Sunday
        # Add individual date gaps (holidays, etc.) to rangebreaks
        if date_gaps:
            rangebreaks_list.append(dict(values=date_gaps))
    
    # Style all subplots
    fig.update_xaxes(
        showgrid=True,
        gridwidth=1,
        gridcolor=COLORS["grid"],
        showline=True,
        linewidth=1,
        linecolor=COLORS["grid"],
        # Hide non-trading days to avoid gaps in the chart
        rangebreaks=rangebreaks_list,
    )
    
    fig.update_yaxes(
        showgrid=True,
        gridwidth=1,
        gridcolor=COLORS["grid"],
        showline=True,
        linewidth=1,
        linecolor=COLORS["grid"],
    )
    
    # Specific styling for price chart (row 1) - with log scale
    fig.update_yaxes(
        title_text="Price ($)",
        title_font=dict(size=10, color=COLORS["muted_text"]),
        type="log",  # Set logarithmic scale for price chart
        row=1, col=1
    )
    
    # Specific styling for volume chart (row 2)
    fig.update_yaxes(
        title_text="Vol",
        title_font=dict(size=10, color=COLORS["muted_text"]),
        showgrid=False,
        row=2, col=1
    )
    
    # Specific styling for RS chart (row 3)
    fig.update_yaxes(
        title_text="RS Ratio",
        title_font=dict(size=10, color=COLORS["muted_text"]),
        row=3, col=1
    )
    
    # Specific styling for RSI chart (row 4)
    fig.update_yaxes(
        title_text="RSI",
        title_font=dict(size=10, color=COLORS["muted_text"]),
        range=[0, 100],  # RSI is always 0-100
        row=4, col=1
    )
    
    # Add horizontal lines for RSI levels
    for level, color, dash in [
        (80, '#22c55e', 'dot'),   # Upper Bull (green)
        (60, '#ef4444', 'dot'),   # Upper Bear (red)
        (40, '#22c55e', 'dot'),   # Lower Bull (green)
        (20, '#ef4444', 'dot'),   # Lower Bear (red)
    ]:
        fig.add_hline(
            y=level,
            line=dict(color=color, width=1, dash=dash),
            row=4, col=1
        )
    
    # Format x-axis dates (only on bottom subplot)
    fig.update_xaxes(
        title_text="Date",
        title_font=dict(size=10, color=COLORS["muted_text"]),
        tickformat="%b %Y",
        row=4, col=1
    )
    
    # Update subplot titles styling
    for annotation in fig['layout']['annotations']:
        annotation['font'] = dict(size=11, color=COLORS["muted_text"])
    
    return fig
