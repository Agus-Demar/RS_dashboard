"""
Main dashboard layout.

Defines the structure of the RS Dashboard including:
- Header
- Filter controls
- Heatmap
- Detail panel
"""
from dash import html, dcc
import dash_bootstrap_components as dbc


def create_layout():
    """
    Create the main dashboard layout.
    
    Returns:
        Dash layout component
    """
    return dbc.Container([
        # Initial Loading Overlay (shown before first callback completes)
        html.Div(
            id="initial-loading-overlay",
            children=[
                html.Div([
                    html.Div([
                        html.H2("📊 RS Industry Dashboard", className="text-light mb-4"),
                        html.Div([
                            dbc.Spinner(color="success", size="lg", spinner_class_name="me-3"),
                            html.Span("Loading data...", className="text-light fs-5"),
                        ], className="d-flex align-items-center justify-content-center mb-4"),
                        dbc.Progress(
                            value=100,
                            animated=True,
                            striped=True,
                            color="success",
                            style={"height": "6px", "width": "350px"},
                            className="mb-3"
                        ),
                        html.P("Fetching RS data for 127 sub-industries...", 
                               className="text-muted small mb-0"),
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
        
        # Header
        dbc.Row([
            dbc.Col([
                html.H1(
                    "📊 Relative Strength Industry Dashboard",
                    className="text-center mt-4 mb-2"
                ),
                html.P(
                    "Mansfield RS by GICS Sub-Industry | Weekly Analysis",
                    className="text-center text-muted mb-4"
                ),
            ])
        ]),
        
        # Filter Controls Row
        dbc.Row([
            # Sector Filter
            dbc.Col([
                html.Label("Filter by Sector:", className="fw-bold mb-1"),
                dcc.Dropdown(
                    id="sector-filter",
                    options=[],  # Populated by callback
                    multi=True,
                    placeholder="All Sectors",
                    className="mb-3",
                    style={"color": "#333"}
                ),
            ], md=4),
            
            # Sort Method
            dbc.Col([
                html.Label("Sort By:", className="fw-bold mb-1"),
                dbc.RadioItems(
                    id="sort-method",
                    options=[
                        {"label": " Latest RS", "value": "latest"},
                        {"label": " 4W Change", "value": "change"},
                        {"label": " Sector", "value": "sector"},
                        {"label": " A-Z", "value": "alpha"},
                    ],
                    value="latest",
                    inline=True,
                    className="mb-3"
                ),
            ], md=4),
            
            # Weeks Slider
            dbc.Col([
                html.Label("Weeks to Display:", className="fw-bold mb-1"),
                dcc.Slider(
                    id="weeks-slider",
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
            ], md=4),
        ], className="mb-4 p-3 bg-dark rounded"),
        
        # Sector Heatmap (above main heatmap)
        dbc.Row([
            dbc.Col([
                html.Div(
                    id="sector-heatmap-container",
                    style={
                        "border": "1px solid #334155",
                        "borderRadius": "8px",
                        "backgroundColor": "#0f172a",
                        "marginBottom": "1rem",
                    },
                    children=[
                        dcc.Graph(
                            id="sector-heatmap",
                            config={
                                "displayModeBar": True,
                                "scrollZoom": False,
                                "displaylogo": False,
                                "modeBarButtonsToRemove": [
                                    "select2d", "lasso2d", "autoScale2d", "zoomOut2d"
                                ],
                            },
                        )
                    ]
                )
            ])
        ]),
        
        # Loading indicator and Sub-Industry Heatmap
        dbc.Row([
            dbc.Col([
                dcc.Loading(
                    id="loading-heatmap",
                    type="default",
                    color="#22c55e",
                    fullscreen=True,
                    style={"backgroundColor": "rgba(15, 23, 42, 0.9)"},
                    children=[
                        # Custom loading overlay content
                        html.Div(
                            id="loading-overlay",
                            children=[
                                html.Div([
                                    html.H4("📊 Loading RS Data...", className="text-light mb-3"),
                                    dbc.Progress(
                                        id="loading-progress",
                                        value=100,
                                        animated=True,
                                        striped=True,
                                        color="success",
                                        style={"height": "8px", "width": "300px"},
                                        className="mb-2"
                                    ),
                                    html.P("Fetching sub-industry data", className="text-muted small"),
                                ], className="text-center", style={"display": "none"})
                            ]
                        ),
                        # Sub-Industry Heatmap container - no fixed height, let figure control size
                        html.Div(
                            id="heatmap-scroll-container",
                            style={
                                "border": "1px solid #334155",
                                "borderRadius": "8px",
                                "backgroundColor": "#0f172a",
                            },
                            children=[
                                dcc.Graph(
                                    id="rs-heatmap",
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
                    id="detail-panel",
                    className="p-3 bg-dark border border-secondary rounded",
                    children=[
                        html.P(
                            "📈 Click chart icon to see sector ETF | Click cell to drill down to stocks",
                            className="text-muted text-center mb-0"
                        )
                    ]
                )
            ])
        ], className="mt-4"),
        
        # TradingView Chart Container (shown on cell click)
        dbc.Row([
            dbc.Col([
                html.Div(
                    id="tradingview-container",
                    className="mt-5 pt-3",  # Increased margin for clear separation
                    style={"display": "none"},
                    children=[
                        html.H5(
                            id="tradingview-title",
                            className="text-center mb-3"
                        ),
                        html.Iframe(
                            id="tradingview-iframe",
                            src="",
                            style={
                                "width": "100%",
                                "height": "500px",
                                "border": "1px solid #334155",
                                "borderRadius": "8px",
                            }
                        )
                    ]
                )
            ])
        ]),
        
        # Data Statistics (footer)
        dbc.Row([
            dbc.Col([
                html.Div(
                    id="data-stats",
                    className="text-center text-muted mt-4 mb-3 small"
                )
            ])
        ]),
        
        # Hidden data stores
        dcc.Store(id="rs-data-store"),
        dcc.Store(id="sector-data-store"),  # Store for sector name to code mapping
        dcc.Store(id="selected-cell-store"),
        
    ], fluid=True, className="bg-dark text-light min-vh-100 pb-4")

