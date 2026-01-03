"""
Shared heatmap configuration constants.

Ensures consistent layout and styling across both main and stock heatmaps.
"""

# Row height in pixels - must be large enough to prevent y-axis label overlap
# 32px provides good spacing for labels
ROW_HEIGHT = 32

# Chart column identifier
CHART_COLUMN = "📈"

# Maximum label length before truncation
MAX_LABEL_LENGTH = 45

# Layout margins
MARGINS = {
    "left": 300,      # Space for y-axis labels (sub-industry names)
    "right": 80,      # Space for chart column and colorbar
    "top": 120,       # Space for title and legend (increased for better spacing)
    "bottom": 80,     # Space for x-axis labels (weeks)
}

# Stock heatmap margins (smaller left margin for ticker symbols)
STOCK_MARGINS = {
    "left": 120,
    "right": 80,
    "top": 120,       # Same as main heatmap for consistency
    "bottom": 80,
}

# Minimum chart heights
MIN_CHART_HEIGHT = 400
MIN_MAIN_CHART_HEIGHT = 600

# Colors
COLORS = {
    "paper_bg": "#0f172a",    # Slate 900
    "plot_bg": "#1e293b",     # Slate 800
    "grid": "#334155",        # Slate 700
    "text": "#e2e8f0",        # Slate 200
    "muted_text": "#94a3b8",  # Slate 400
    "title": "#f8fafc",       # Slate 50
    "chart_col_bg": "#1e293b",  # Dark slate for chart column background
}

# Font sizes
FONT_SIZES = {
    "title": 20,
    "subtitle": 18,
    "axis_label": 10,
    "stock_axis_label": 11,
    "legend": 12,
    "chart_icon": 14,
}
