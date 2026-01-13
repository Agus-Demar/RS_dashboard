"""
Ticker searcher page layout.

Allows searching by ticker to find its sub-industry and display:
- Sub-industry RS heatmap for all stocks in that sub-industry
- Daily/Weekly price chart with RS indicator for the searched ticker
"""
from dash import html, dcc
import dash_bootstrap_components as dbc


def create_layout(ticker: str = None):
    """
    Create the ticker searcher page layout.
    
    Args:
        ticker: Optional initial ticker to search for
    
    Returns:
        Dash layout component
    """
    return dbc.Container([
        # Store the ticker for callbacks
        dcc.Store(id="ticker-search-value", data=ticker),
        dcc.Store(id="ticker-subindustry-code", data=None),
        dcc.Store(id="ticker-selected-stock-store", data=None),
        
        # Header with Back Button
        dbc.Row([
            dbc.Col([
                html.Div([
                    # Back button (positioned absolutely)
                    dcc.Link(
                        dbc.Button(
                            [html.I(className="fas fa-arrow-left me-2"), "Back to Main"],
                            id="ticker-back-button",
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
                    
                    # Title
                    html.H1(
                        "🔍 Ticker Searcher",
                        className="text-center mt-4 mb-2"
                    ),
                    html.P(
                        "Search by ticker to view its sub-industry heatmap and RS indicators",
                        className="text-center text-muted mb-4"
                    ),
                ], className="position-relative")
            ])
        ]),
        
        # Search Bar Row
        dbc.Row([
            dbc.Col([
                dbc.InputGroup([
                    dbc.InputGroupText(
                        html.I(className="fas fa-search"),
                        className="bg-secondary border-secondary"
                    ),
                    dbc.Input(
                        id="ticker-search-input",
                        type="text",
                        placeholder="Enter ticker symbol (e.g., AAPL, MSFT, GOOGL)...",
                        value=ticker or "",
                        debounce=True,
                        className="bg-dark text-light border-secondary",
                        style={"fontSize": "1.1rem"}
                    ),
                    dbc.Button(
                        "Search",
                        id="ticker-search-button",
                        color="success",
                        className="px-4"
                    ),
                ], size="lg")
            ], md=8, className="mx-auto")
        ], className="mb-4 p-3 bg-dark rounded"),
        
        # Search Result Info
        dbc.Row([
            dbc.Col([
                html.Div(
                    id="ticker-search-result",
                    className="text-center mb-4"
                )
            ])
        ]),
        
        # Filter Controls Row (only shown when ticker is found)
        html.Div(
            id="ticker-controls-container",
            style={"display": "none"},
            children=[
                dbc.Row([
                    # Sort Method
                    dbc.Col([
                        html.Label("Sort By:", className="fw-bold mb-1"),
                        dbc.RadioItems(
                            id="ticker-sort-method",
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
                            id="ticker-weeks-slider",
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
            ]
        ),
        
        # Sub-Industry Heatmap (shown when ticker is found)
        html.Div(
            id="ticker-heatmap-container",
            style={"display": "none"},
            children=[
                dbc.Row([
                    dbc.Col([
                        dcc.Loading(
                            id="loading-ticker-heatmap",
                            type="default",
                            color="#22c55e",
                            children=[
                                html.Div(
                                    id="ticker-heatmap-scroll-container",
                                    style={
                                        "border": "1px solid #334155",
                                        "borderRadius": "8px",
                                        "backgroundColor": "#0f172a",
                                    },
                                    children=[
                                        dcc.Graph(
                                            id="ticker-rs-heatmap",
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
            ]
        ),
        
        # Detail Panel (shown on cell click)
        html.Div(
            id="ticker-detail-container",
            style={"display": "none"},
            children=[
                dbc.Row([
                    dbc.Col([
                        html.Div(
                            id="ticker-detail-panel",
                            className="p-3 bg-dark border border-secondary rounded",
                            children=[
                                html.P(
                                    "Click on a stock in the heatmap to see its price chart with RS indicator",
                                    className="text-muted text-center mb-0"
                                )
                            ]
                        )
                    ])
                ], className="mt-4"),
            ]
        ),
        
        # Stock Price + RS Chart Container (shown on cell click or for searched ticker)
        dbc.Row([
            dbc.Col([
                html.Div(
                    id="ticker-chart-container",
                    className="mt-5 pt-3",
                    style={"display": "none"},
                    children=[
                        html.H5(
                            id="ticker-chart-title",
                            className="text-center mb-3"
                        ),
                        # Daily/Weekly timeframe tabs
                        dbc.Tabs(
                            id="ticker-chart-timeframe-tabs",
                            active_tab="daily",
                            className="mb-3",
                            children=[
                                dbc.Tab(label="Daily", tab_id="daily"),
                                dbc.Tab(label="Weekly", tab_id="weekly"),
                            ]
                        ),
                        dcc.Loading(
                            id="loading-ticker-chart",
                            type="default",
                            color="#22c55e",
                            children=[
                                dcc.Graph(
                                    id="ticker-price-rs-chart",
                                    config={
                                        "displayModeBar": True,
                                        "scrollZoom": True,
                                        "displaylogo": False,
                                        "modeBarButtonsToRemove": [
                                            "select2d", "lasso2d"
                                        ],
                                    },
                                    style={
                                        "height": "1000px",
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
                    id="ticker-data-stats",
                    className="text-center text-muted mt-4 mb-3 small"
                )
            ])
        ]),
        
    ], fluid=True, className="bg-dark text-light min-vh-100 pb-4")
