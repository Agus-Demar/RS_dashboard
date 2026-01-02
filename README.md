# RS Dashboard

**Relative Strength Industry Dashboard** - An interactive visualization of Mansfield Relative Strength by GICS Sub-Industry.

![Python](https://img.shields.io/badge/python-3.11+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109+-green.svg)
![Dash](https://img.shields.io/badge/Dash-2.14+-purple.svg)

## Overview

This application calculates and displays **Mansfield Relative Strength (RS)** for GICS sub-industries, helping identify which sectors of the market are outperforming or underperforming the S&P 500 benchmark.

### Key Features

- **Interactive Heatmap**: Visualize RS across ~80 sub-industries and 17+ weeks
- **Real-time Filtering**: Filter by sector, sort by various criteria
- **Weekly Calculations**: Automated RS calculations every Saturday
- **REST API**: Full API access to RS data
- **Free Data Sources**: Uses yfinance and Wikipedia (no API keys required)

### What is Mansfield Relative Strength?

Mansfield RS is a normalized measure of relative performance:

```
RS Line = (Asset Price / Benchmark Price) × 100
RS SMA = 52-week Simple Moving Average of RS Line
Mansfield RS = ((RS Line - RS SMA) / RS SMA) × 100
```

**Interpretation:**
- **> +10**: Strong outperformance
- **+5 to +10**: Moderate outperformance  
- **-5 to +5**: Neutral (in-line with market)
- **-10 to -5**: Moderate underperformance
- **< -10**: Strong underperformance

## Quick Start

### 1. Clone and Setup

```bash
# Clone the repository
git clone <repository-url>
cd RS_dashboard

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment template
cp .env.example .env
```

### 2. Bootstrap Data

This fetches S&P 500 constituents, 2 years of price history, and calculates initial RS values:

```bash
python -m scripts.bootstrap_data
```

This process takes approximately 10-15 minutes depending on your internet connection.

### 3. Start the Application

```bash
uvicorn src.main:app --reload
```

### 4. Access the Dashboard

- **Dashboard**: http://localhost:8000/dashboard/
- **API Docs**: http://localhost:8000/api/docs
- **Health Check**: http://localhost:8000/health

## Project Structure

```
rs_dashboard/
├── src/
│   ├── main.py              # FastAPI application entry
│   ├── config.py            # Configuration settings
│   ├── models/              # SQLAlchemy database models
│   ├── services/            # Business logic (RS calculator, aggregator)
│   ├── ingestion/           # Data fetching (yfinance, Wikipedia)
│   ├── dashboard/           # Plotly Dash application
│   ├── api/                 # REST API endpoints
│   └── jobs/                # Scheduled tasks
├── scripts/
│   ├── bootstrap_data.py    # Initial data population
│   ├── backfill_rs.py       # Historical RS calculation
│   └── run_job.py           # Manual job runner
├── data/                    # SQLite database (created automatically)
├── requirements.txt
├── .env.example
└── README.md
```

## Dashboard Usage

### Heatmap Layout

- **X-axis (horizontal)**: Weeks - most recent on the LEFT
- **Y-axis (vertical)**: GICS Sub-Industries (~80 rows)
- **Colors**: 
  - 🟢 Green: Strong (top 33%)
  - 🟡 Yellow: Neutral (middle 34%)
  - 🔴 Red: Weak (bottom 33%)

### Controls

- **Sector Filter**: Multi-select to focus on specific sectors
- **Sort By**:
  - Latest RS: Sort by most recent week's strength
  - 4W Change: Sort by 4-week momentum change
  - Sector: Group by GICS sector
  - A-Z: Alphabetical
- **Weeks Slider**: Adjust time range (4-26 weeks)

### Interactivity

- **Hover**: See detailed RS information
- **Click**: View constituent stocks in the sub-industry
- **Zoom/Pan**: Navigate the large matrix

## API Endpoints

### RS Data

```
GET /api/rs/matrix           # Heatmap matrix data
GET /api/rs/subindustry/{code}  # RS history for sub-industry
GET /api/rs/week/{date}      # All RS for specific week
GET /api/rs/latest-week      # Latest available week
```

### GICS Classification

```
GET /api/gics/sectors        # List of sectors
GET /api/gics/subindustries  # All sub-industries
GET /api/gics/subindustry/{code}/stocks  # Stocks in sub-industry
```

### System

```
GET /health                  # Health check
GET /api/status              # Data statistics
```

## Scheduled Jobs

The application runs two scheduled jobs (when `SCHEDULER_ENABLED=true`):

| Job | Schedule | Description |
|-----|----------|-------------|
| Weekly RS | Saturday 6 AM ET | Calculates Mansfield RS for all sub-industries |
| Daily Prices | Mon-Fri 7 PM ET | Fetches latest price data |

### Manual Job Execution

```bash
# Run weekly RS calculation
python -m scripts.run_job weekly

# Run daily price refresh
python -m scripts.run_job daily

# Run both
python -m scripts.run_job both
```

## Configuration

Key settings in `.env`:

| Variable | Default | Description |
|----------|---------|-------------|
| `DATABASE_URL` | `sqlite:///data/rs_dashboard.db` | Database connection |
| `BENCHMARK_TICKER` | `SPY` | Benchmark for RS calculation |
| `RS_SMA_PERIOD_WEEKS` | `52` | SMA period for Mansfield RS |
| `DEFAULT_WEEKS_DISPLAY` | `17` | Default weeks in dashboard |
| `SCHEDULER_ENABLED` | `true` | Enable scheduled jobs |

## Data Sources

All data sources are **FREE** with no API keys required:

| Source | Data | Notes |
|--------|------|-------|
| **yfinance** | Historical prices | Unlimited, ~2000 req/hr |
| **Wikipedia** | S&P 500 constituents, GICS | Real-time updates |

## Development

### Running Tests

```bash
pytest tests/
```

### Rebuilding RS Data

If you need to recalculate RS values:

```bash
# Backfill last 26 weeks
python -m scripts.backfill_rs --weeks 26

# Backfill from specific date
python -m scripts.backfill_rs --from-date 2024-01-01
```

### Database Reset

To start fresh:

```bash
rm data/rs_dashboard.db
python -m scripts.bootstrap_data
```

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     RS Dashboard                             │
├─────────────────────────────────────────────────────────────┤
│  Data Layer         Processing         Presentation         │
│  ────────────       ──────────         ────────────         │
│  • yfinance     →   • RS Calculator  → • Dash Heatmap      │
│  • Wikipedia    →   • Aggregator     → • FastAPI REST      │
│  • SQLite DB    →   • Percentile     → • Interactive UI    │
│                                                              │
│  Scheduler                                                   │
│  ─────────                                                   │
│  • Weekly RS (Sat 6AM)                                      │
│  • Daily Prices (Mon-Fri 7PM)                               │
└─────────────────────────────────────────────────────────────┘
```

## Troubleshooting

### "No RS data available"

Run the bootstrap or backfill script:
```bash
python -m scripts.bootstrap_data
```

### "Rate limit exceeded"

The app uses conservative rate limiting. Wait a few minutes and try again.

### Database locked

SQLite can only handle one write at a time. Stop other processes and try again.

## License

MIT License

## Acknowledgments

- [Stan Weinstein](https://en.wikipedia.org/wiki/Stan_Weinstein) for the Mansfield RS methodology
- [yfinance](https://github.com/ranaroussi/yfinance) for free market data
- [Plotly Dash](https://dash.plotly.com/) for interactive visualizations

