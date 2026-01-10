"""
Stock drilldown page layout.

Displays individual stock RS heatmap for a specific GICS sub-industry.
Similar structure to main layout but focused on individual stocks.
"""
from dash import html, dcc
import dash_bootstrap_components as dbc


def create_layout(subindustry_code: str = None):
    """
    Create the stock drilldown page layout.
    
    Args:
        subindustry_code: GICS sub-industry code to display stocks for
    
    Returns:
        Dash layout component
    """
    return dbc.Container([
        # Store the subindustry code for callbacks
        dcc.Store(id="stock-subindustry-code", data=subindustry_code),
        
        # Initial Loading Overlay
        html.Div(
            id="stock-loading-overlay",
            children=[
                html.Div([
                    html.Div([
                        html.H2("📊 Loading Stock Data...", className="text-light mb-4"),
                        html.Div([
                            dbc.Spinner(color="success", size="lg", spinner_class_name="me-3"),
                            html.Span("Calculating RS for stocks...", className="text-light fs-5"),
                        ], className="d-flex align-items-center justify-content-center mb-4"),
                        dbc.Progress(
                            value=100,
                            animated=True,
                            striped=True,
                            color="success",
                            style={"height": "6px", "width": "350px"},
                            className="mb-3"
                        ),
                    ], className="text-center")
                ], className="d-flex align-items-center justify-content-center", 
                   style={"minHeight": "100vh"})
            ],
            style={
                "position": "fixed",
                "top": 0,
                "left": 0,
                "width": "100%",
                "height": "100%",
                "backgroundColor": "#0f172a",
                "zIndex": 9999,
                "display": "block"
            }
        ),
        
        # Header with Back Button
        dbc.Row([
            dbc.Col([
                html.Div([
                    # Back button (positioned absolutely)
                    dcc.Link(
                        dbc.Button(
                            [html.I(className="fas fa-arrow-left me-2"), "Back to Main"],
                            id="back-button",
                            color="secondary",
                            size="sm",
                        ),
                        href="/dashboard/",
                        refresh=False,
                        style={
                            "position": "absolute",
                            "top": "1rem",
                            "right": "1rem",
                            "zIndex": 100
                        }
                    ),
                    
                    # Title (will be updated by callback with sub-industry name)
                    html.H1(
                        id="stock-page-title",
                        children="📈 Stock RS Heatmap",
                        className="text-center mt-4 mb-2"
                    ),
                    html.P(
                        id="stock-page-subtitle",
                        children="Individual Stock Relative Strength | Click stock for TradingView chart",
                        className="text-center text-muted mb-4"
                    ),
                ], className="position-relative")
            ])
        ]),
        
        # Filter Controls Row (simplified for stocks)
        dbc.Row([
            # Sort Method
            dbc.Col([
                html.Label("Sort By:", className="fw-bold mb-1"),
                dbc.RadioItems(
                    id="stock-sort-method",
                    options=[
                        {"label": " Latest RS", "value": "latest"},
                        {"label": " 4W Change", "value": "change"},
                        {"label": " A-Z", "value": "alpha"},
                    ],
                    value="latest",
                    inline=True,
                    className="mb-3"
                ),
            ], md=6),
            
            # Weeks Slider
            dbc.Col([
                html.Label("Weeks to Display:", className="fw-bold mb-1"),
                dcc.Slider(
                    id="stock-weeks-slider",
                    min=4,
                    max=26,
                    step=1,
                    value=17,
                    marks={
                        4: '4w',
                        8: '8w',
                        13: '13w',
                        17: '17w',
                        26: '26w'
                    },
                    tooltip={"placement": "bottom", "always_visible": False},
                ),
            ], md=6),
        ], className="mb-4 p-3 bg-dark rounded"),
        
        # Loading indicator and Stock Heatmap
        dbc.Row([
            dbc.Col([
                dcc.Loading(
                    id="loading-stock-heatmap",
                    type="default",
                    color="#22c55e",
                    fullscreen=True,
                    style={"backgroundColor": "rgba(15, 23, 42, 0.9)"},
                    children=[
                        # Heatmap container - no fixed height, let figure control size
                        html.Div(
                            id="stock-heatmap-scroll-container",
                            style={
                                "border": "1px solid #334155",
                                "borderRadius": "8px",
                                "backgroundColor": "#0f172a",
                            },
                            children=[
                                dcc.Graph(
                                    id="stock-rs-heatmap",
                                    config={
                                        "displayModeBar": True,
                                        "scrollZoom": False,
                                        "displaylogo": False,
                                        "modeBarButtonsToRemove": [
                                            "select2d", "lasso2d", "autoScale2d", "zoomOut2d"
                                        ],
                                    },
                                    # Height is controlled by the figure layout
                                )
                            ]
                        )
                    ]
                )
            ])
        ]),
        
        # Color Legend
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.Span("🔴 Weak (Bottom 33%)", className="mx-3"),
                    html.Span("🟡 Neutral (Middle 34%)", className="mx-3"),
                    html.Span("🟢 Strong (Top 33%)", className="mx-3"),
                ], className="text-center my-3")
            ])
        ]),
        
        # Detail Panel (shown on cell click)
        dbc.Row([
            dbc.Col([
                html.Div(
                    id="stock-detail-panel",
                    className="p-3 bg-dark border border-secondary rounded",
                    children=[
                        html.P(
                            "Click on a stock to see TradingView chart",
                            className="text-muted text-center mb-0"
                        )
                    ]
                )
            ])
        ], className="mt-4"),
        
        # Stock Price + RS Chart Container (shown on cell click)
        dbc.Row([
            dbc.Col([
                html.Div(
                    id="stock-chart-container",
                    className="mt-5 pt-3",
                    style={"display": "none"},
                    children=[
                        html.H5(
                            id="stock-chart-title",
                            className="text-center mb-3"
                        ),
                        # Daily/Weekly timeframe tabs
                        dbc.Tabs(
                            id="chart-timeframe-tabs",
                            active_tab="daily",
                            className="mb-3",
                            children=[
                                dbc.Tab(label="Daily", tab_id="daily"),
                                dbc.Tab(label="Weekly", tab_id="weekly"),
                            ]
                        ),
                        dcc.Loading(
                            id="loading-stock-chart",
                            type="default",
                            color="#22c55e",
                            children=[
                                dcc.Graph(
                                    id="stock-price-rs-chart",
                                    config={
                                        "displayModeBar": True,
                                        "scrollZoom": True,
                                        "displaylogo": False,
                                        "modeBarButtonsToRemove": [
                                            "select2d", "lasso2d"
                                        ],
                                    },
                                    style={
                                        "height": "1000px",  # Increased for 4 subplots (Price, Volume, RS, RSI)
                                        "border": "1px solid #334155",
                                        "borderRadius": "8px",
                                    }
                                )
                            ]
                        )
                    ]
                )
            ])
        ]),
        
        # Data Statistics (footer)
        dbc.Row([
            dbc.Col([
                html.Div(
                    id="stock-data-stats",
                    className="text-center text-muted mt-4 mb-3 small"
                )
            ])
        ]),
        
        # Hidden store for selected stock info (used for tab switching)
        dcc.Store(id="selected-stock-store"),
        
    ], fluid=True, className="bg-dark text-light min-vh-100 pb-4")

