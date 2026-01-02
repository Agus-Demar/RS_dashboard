"""
Color utilities for the RS heatmap.

Provides color scales and mapping functions for RS percentile visualization.
"""
from typing import List, Tuple


def get_color_scale() -> List[List]:
    """
    Get the color scale for RS heatmap.
    
    Maps percentiles to colors:
    - 0-33: Red (weak/underperforming)
    - 33-67: Yellow (neutral)
    - 67-100: Green (strong/outperforming)
    
    Returns:
        List of [position, color] pairs for Plotly colorscale
    """
    return [
        [0.00, "#b91c1c"],   # Dark red (0th percentile)
        [0.15, "#dc2626"],   # Red
        [0.25, "#ef4444"],   # Light red
        [0.33, "#f97316"],   # Orange (weak/neutral boundary)
        [0.42, "#f59e0b"],   # Amber
        [0.50, "#eab308"],   # Yellow (50th percentile)
        [0.58, "#facc15"],   # Light yellow
        [0.67, "#84cc16"],   # Lime (neutral/strong boundary)
        [0.75, "#22c55e"],   # Green
        [0.85, "#16a34a"],   # Dark green
        [1.00, "#15803d"],   # Darkest green (100th percentile)
    ]


def percentile_to_rgb(percentile: float) -> Tuple[int, int, int]:
    """
    Convert RS percentile (0-100) to RGB color.
    
    Args:
        percentile: Value from 0 to 100
    
    Returns:
        Tuple of (R, G, B) values
    """
    # Clamp to valid range
    percentile = max(0, min(100, percentile))
    
    if percentile <= 33:
        # Red to Orange gradient
        ratio = percentile / 33
        r = 220
        g = int(38 + (118 * ratio))  # 38 -> 156
        b = 38
    elif percentile <= 67:
        # Orange to Yellow to Lime gradient
        ratio = (percentile - 33) / 34
        if ratio < 0.5:
            # Orange to Yellow
            sub_ratio = ratio * 2
            r = int(249 - (15 * sub_ratio))  # 249 -> 234
            g = int(115 + (64 * sub_ratio))  # 115 -> 179
            b = int(22 + (6 * sub_ratio))    # 22 -> 28
        else:
            # Yellow to Lime
            sub_ratio = (ratio - 0.5) * 2
            r = int(234 - (102 * sub_ratio))  # 234 -> 132
            g = int(179 + (25 * sub_ratio))   # 179 -> 204
            b = int(28 + (6 * sub_ratio))     # 28 -> 34
    else:
        # Lime to Green gradient
        ratio = (percentile - 67) / 33
        r = int(132 - (111 * ratio))  # 132 -> 21
        g = int(204 - (41 * ratio))   # 204 -> 163
        b = int(34 + (27 * ratio))    # 34 -> 61
    
    return (int(r), int(g), int(b))


def percentile_to_hex(percentile: float) -> str:
    """
    Convert RS percentile to hex color string.
    
    Args:
        percentile: Value from 0 to 100
    
    Returns:
        Hex color string (e.g., "#22c55e")
    """
    r, g, b = percentile_to_rgb(percentile)
    return f"#{r:02x}{g:02x}{b:02x}"


def get_strength_label(percentile: float) -> str:
    """
    Get strength label for a percentile value.
    
    Args:
        percentile: Value from 0 to 100
    
    Returns:
        String label: "Strong", "Neutral", or "Weak"
    """
    if percentile is None:
        return "N/A"
    if percentile >= 67:
        return "Strong 💪"
    elif percentile >= 33:
        return "Neutral ➖"
    else:
        return "Weak 📉"


def get_strength_emoji(percentile: float) -> str:
    """
    Get emoji for percentile value.
    
    Args:
        percentile: Value from 0 to 100
    
    Returns:
        Emoji string
    """
    if percentile is None:
        return "❓"
    if percentile >= 67:
        return "🟢"
    elif percentile >= 33:
        return "🟡"
    else:
        return "🔴"

