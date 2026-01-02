# Relative Strength (RS) Industry Dashboard — Complete Specification

> **Purpose**: This document serves as the definitive reference for building an interactive dashboard that displays Mansfield Relative Strength (RS) by GICS Sub-Industry. Use this as context when prompting an AI to build the application.

---

## Table of Contents

1. [Concept: Mansfield Relative Strength](#1-concept-mansfield-relative-strength)
2. [Tech Stack](#2-tech-stack)
3. [Project Structure](#3-project-structure)
4. [Database Schema](#4-database-schema)
5. [Data Ingestion Module](#5-data-ingestion-module)
6. [RS Calculation Engine](#6-rs-calculation-engine)
7. [Weekly Job Scheduler](#7-weekly-job-scheduler)
8. [Dashboard Specifications](#8-dashboard-specifications)
9. [API Endpoints](#9-api-endpoints)
10. [Configuration & Environment](#10-configuration--environment)
11. [Implementation Checklist](#11-implementation-checklist)

---

## 1. Concept: Mansfield Relative Strength

### What is Relative Strength (RS)?

Relative Strength (RS) is a **momentum-based comparative metric** that measures a stock's or sector's price performance RELATIVE to a benchmark (typically the S&P 500).

> ⚠️ **CRITICAL DISTINCTION**: RS ≠ RSI
> - **Relative Strength (RS)**: Compares an asset's performance TO the market benchmark
> - **Relative Strength Index (RSI)**: A momentum oscillator (0-100 scale) measuring speed/magnitude of price changes

### Mansfield Relative Strength Calculation (3-Step Process)

This application uses the **Mansfield Relative Strength** method, developed by Stan Weinstein:

```
Step 1: Calculate the Raw RS Line
─────────────────────────────────
RS_Line(t) = (Price_Asset(t) / Price_Benchmark(t)) × 100

Step 2: Compute the Moving Average of RS Line
─────────────────────────────────────────────
RS_MA(t) = SMA(RS_Line, 52 weeks)   // 52-week Simple Moving Average

Step 3: Calculate Mansfield RS (Normalized)
───────────────────────────────────────────
Mansfield_RS(t) = ((RS_Line(t) - RS_MA(t)) / RS_MA(t)) × 100
```

### Interpretation Scale

| Mansfield RS Value | Interpretation |
|--------------------|----------------|
| > +10 | Strong outperformance (bullish momentum) |
| +5 to +10 | Moderate outperformance |
| -5 to +5 | Neutral / In-line with market |
| -10 to -5 | Moderate underperformance |
| < -10 | Strong underperformance (bearish momentum) |

### Why Mansfield RS?

1. **Normalized**: Zero-centered, comparable across different assets
2. **Trend-aware**: Incorporates 52-week historical context
3. **Mean-reverting context**: Shows deviation from "normal" relative performance
4. **Actionable thresholds**: Clear buy/sell zones based on deviation

---

## 2. Tech Stack

### Core Technologies

| Layer | Technology | Purpose |
|-------|------------|---------|
| **Language** | Python 3.11+ | Primary development language |
| **Web Framework** | FastAPI | REST API, async support, auto-docs |
| **Dashboard** | Plotly Dash | Interactive visualizations |
| **Database** | PostgreSQL + TimescaleDB | Time-series optimized storage |
| **ORM** | SQLAlchemy 2.0 | Database abstraction |
| **Migrations** | Alembic | Schema version control |
| **Scheduler** | APScheduler | Weekly job execution |
| **Cache** | Redis | Computed RS caching |
| **Containerization** | Docker + docker-compose | Deployment |

### Data Processing

| Library | Purpose |
|---------|---------|
| pandas | Data manipulation, time-series |
| numpy | Numerical computations |
| python-dateutil | Date handling |

### Data Sources (FREE APIs)

| Source | Use Case | Rate Limit | API Key Required |
|--------|----------|------------|------------------|
| **yfinance** | Price data (primary) | ~2000/hr | ❌ No |
| **Wikipedia** | S&P 500 constituents + GICS | Unlimited | ❌ No |
| **Financial Modeling Prep** | GICS mapping, screening | 250/day | ✅ Yes (free tier) |
| **Alpha Vantage** | Backup price source | 25/day | ✅ Yes (free tier) |

### Visualization

| Library | Purpose |
|---------|---------|
| plotly | Interactive charts |
| dash | Dashboard framework |
| dash-bootstrap-components | UI components, theming |

---

## 3. Project Structure

```
rs_dashboard/
│
├── docker-compose.yml              # Container orchestration
├── Dockerfile                      # App container definition
├── requirements.txt                # Python dependencies
├── alembic.ini                     # Alembic configuration
├── .env.example                    # Environment template
├── README.md                       # Project documentation
│
├── alembic/                        # Database migrations
│   ├── versions/                   # Migration scripts
│   └── env.py                      # Alembic environment
│
├── src/
│   ├── __init__.py
│   ├── main.py                     # FastAPI app entry point
│   ├── config.py                   # Application configuration
│   │
│   ├── models/                     # SQLAlchemy ORM models
│   │   ├── __init__.py
│   │   ├── base.py                 # Base model, mixins
│   │   ├── gics.py                 # GICS classification
│   │   ├── stock.py                # Stock master data
│   │   ├── price.py                # Historical prices
│   │   ├── rs_weekly.py            # Weekly RS calculations
│   │   └── job_log.py              # Job execution tracking
│   │
│   ├── schemas/                    # Pydantic schemas
│   │   ├── __init__.py
│   │   ├── rs.py                   # RS data schemas
│   │   └── gics.py                 # GICS schemas
│   │
│   ├── ingestion/                  # Data Ingestion Module
│   │   ├── __init__.py
│   │   ├── config.py               # API keys, rate limits
│   │   ├── base.py                 # Abstract base fetcher
│   │   ├── sources/
│   │   │   ├── __init__.py
│   │   │   ├── yfinance_source.py  # Yahoo Finance (FREE)
│   │   │   ├── fmp_source.py       # Financial Modeling Prep
│   │   │   └── wikipedia_source.py # S&P 500 + GICS scraping
│   │   ├── mappers/
│   │   │   ├── __init__.py
│   │   │   └── gics_mapper.py      # Ticker → GICS mapping
│   │   ├── pipelines/
│   │   │   ├── __init__.py
│   │   │   ├── initial_load.py     # First-time data population
│   │   │   ├── daily_prices.py     # Daily price updates
│   │   │   └── weekly_rs.py        # Weekly RS calculation
│   │   └── utils/
│   │       ├── rate_limiter.py     # API rate limiting
│   │       └── retry.py            # Retry with backoff
│   │
│   ├── services/                   # Business logic
│   │   ├── __init__.py
│   │   ├── rs_calculator.py        # Mansfield RS computation
│   │   ├── aggregator.py           # Sub-industry aggregation
│   │   └── data_service.py         # Data access layer
│   │
│   ├── jobs/                       # Scheduled tasks
│   │   ├── __init__.py
│   │   ├── scheduler.py            # APScheduler configuration
│   │   └── weekly_rs_job.py        # Main weekly RS job
│   │
│   ├── api/                        # FastAPI routes
│   │   ├── __init__.py
│   │   ├── deps.py                 # Dependencies (DB session)
│   │   └── routes/
│   │       ├── __init__.py
│   │       ├── rs.py               # RS data endpoints
│   │       ├── gics.py             # GICS lookup endpoints
│   │       └── health.py           # Health check
│   │
│   └── dashboard/                  # Plotly Dash application
│       ├── __init__.py
│       ├── app.py                  # Dash app initialization
│       ├── layouts/
│       │   ├── __init__.py
│       │   └── main_layout.py      # Dashboard layout
│       ├── callbacks/
│       │   ├── __init__.py
│       │   └── heatmap_callbacks.py # Interactivity logic
│       └── utils/
│           ├── __init__.py
│           └── colors.py           # Color gradient utilities
│
├── data/                           # Static reference data
│   ├── gics_full_classification.csv    # Complete 163 sub-industries
│   └── ticker_gics_mapping.csv         # Manual ticker mappings
│
├── scripts/                        # Utility scripts
│   ├── bootstrap_data.py           # Initial data population
│   ├── backfill_rs.py              # Historical RS backfill
│   └── refresh_gics.py             # Update GICS mappings
│
└── tests/                          # Test suite
    ├── __init__.py
    ├── test_rs_calculator.py
    ├── test_aggregator.py
    └── test_ingestion.py
```

---

## 4. Database Schema

### Entity Relationship

```
┌─────────────────┐       ┌─────────────────┐       ┌─────────────────┐
│ GICSSubIndustry │───1:N─│      Stock      │───1:N─│   StockPrice    │
│                 │       │                 │       │                 │
│ code (PK)       │       │ ticker (PK)     │       │ id (PK)         │
│ name            │       │ name            │       │ ticker (FK)     │
│ industry_code   │       │ gics_code (FK)  │       │ date            │
│ industry_name   │       │ market_cap      │       │ open/high/low   │
│ sector_code     │       │ is_active       │       │ close/adj_close │
│ sector_name     │       │                 │       │ volume          │
└────────┬────────┘       └─────────────────┘       └─────────────────┘
         │
         │ 1:N
         ▼
┌─────────────────┐       ┌─────────────────┐
│    RSWeekly     │       │     JobLog      │
│                 │       │                 │
│ id (PK)         │       │ id (PK)         │
│ subindustry (FK)│       │ job_name        │
│ week_end_date   │       │ started_at      │
│ rs_line         │       │ completed_at    │
│ rs_line_sma_52w │       │ status          │
│ mansfield_rs    │       │ records_count   │
│ rs_percentile   │       │ error_message   │
│ constituents    │       │                 │
└─────────────────┘       └─────────────────┘
```

### Model Definitions

#### GICSSubIndustry

```python
class GICSSubIndustry(Base):
    __tablename__ = "gics_subindustry"
    
    code: str                    # PK, 8-digit code (e.g., "10101010")
    name: str                    # Sub-industry name
    industry_code: str           # 6-digit industry code
    industry_name: str
    industry_group_code: str     # 4-digit industry group code
    industry_group_name: str
    sector_code: str             # 2-digit sector code
    sector_name: str
```

#### Stock

```python
class Stock(Base, TimestampMixin):
    __tablename__ = "stock"
    
    ticker: str                  # PK (e.g., "AAPL")
    name: str                    # Company name
    gics_subindustry_code: str   # FK → GICSSubIndustry
    market_cap: float            # Latest market cap
    is_active: bool              # Currently tracked
```

#### StockPrice

```python
class StockPrice(Base):
    __tablename__ = "stock_price"
    
    id: int                      # PK, autoincrement
    ticker: str                  # FK → Stock
    date: date                   # Trading date
    open: float
    high: float
    low: float
    close: float
    adj_close: float             # Adjusted for splits/dividends
    volume: int
    
    # Indexes: (ticker, date), (date)
```

#### RSWeekly

```python
class RSWeekly(Base, TimestampMixin):
    __tablename__ = "rs_weekly"
    
    id: int                      # PK, autoincrement
    subindustry_code: str        # FK → GICSSubIndustry
    week_end_date: date          # Friday of the week
    week_start_date: date        # Monday of the week
    
    # Mansfield RS components
    rs_line: float               # Raw RS line value
    rs_line_sma_52w: float       # 52-week SMA of RS line
    mansfield_rs: float          # Final Mansfield RS value
    
    # For color coding
    rs_percentile: int           # 0-100 percentile rank
    
    # Aggregation metadata
    constituents_count: int      # Stocks in calculation
    total_market_cap: float
    
    # Unique constraint: (subindustry_code, week_end_date)
```

#### JobLog

```python
class JobLog(Base):
    __tablename__ = "job_log"
    
    id: int                      # PK
    job_name: str                # Job identifier
    started_at: datetime
    completed_at: datetime
    status: Enum                 # STARTED, SUCCESS, FAILED, PARTIAL
    records_processed: int
    error_message: str           # If failed
    details: str                 # JSON metadata
```

---

## 5. Data Ingestion Module

### Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     DATA INGESTION PIPELINE                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────┐     ┌──────────────┐     ┌──────────────┐    │
│  │   Sources    │────▶│   Mappers    │────▶│  Pipelines   │    │
│  └──────────────┘     └──────────────┘     └──────────────┘    │
│        │                    │                    │              │
│  • yfinance_source    • gics_mapper       • initial_load       │
│  • wikipedia_source                       • daily_prices       │
│  • fmp_source                             • weekly_rs          │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                       Utilities                          │   │
│  │  • rate_limiter.py  • retry.py  • validators.py         │   │
│  └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

### Source: yfinance (Primary - FREE)

```python
class YFinanceSource:
    """
    Yahoo Finance data source via yfinance library.
    
    ✅ Completely FREE - no API key required
    ✅ Reliable historical price data
    ✅ Basic sector/industry info
    ⚠️ Industry names don't match GICS exactly
    """
    
    async def fetch_price_history(ticker, start_date, end_date) -> DataFrame
    async def fetch_company_info(ticker) -> dict
    async def fetch_multiple_prices(tickers, start, end, batch_size=50) -> dict
```

### Source: Wikipedia (S&P 500 + GICS - FREE)

```python
class WikipediaSource:
    """
    Scrape S&P 500 constituents from Wikipedia.
    
    ✅ Completely FREE
    ✅ Includes actual GICS sub-industry names
    ✅ Regularly updated
    """
    
    SP500_URL = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    
    async def fetch_sp500_constituents() -> DataFrame
        # Returns: ticker, name, sector, sub_industry
```

### Source: Financial Modeling Prep (Optional - FREE Tier)

```python
class FMPSource:
    """
    Financial Modeling Prep API.
    
    ✅ FREE tier: 250 API calls/day
    ✅ GICS sector/industry info
    ✅ Stock screener for universe expansion
    """
    
    async def fetch_sp500_constituents() -> DataFrame
    async def fetch_company_profile(ticker) -> dict
    async def fetch_stock_screener(sector, market_cap_min) -> DataFrame
```

### GICS Mapper

```python
class GICSMapper:
    """
    Maps tickers to GICS sub-industries using multiple sources.
    
    Priority:
    1. Manual curated mapping (CSV file)
    2. Wikipedia S&P 500 data (has GICS sub-industry names)
    3. FMP/yfinance sector+industry (approximate)
    """
    
    def map_ticker(ticker) -> dict
        # Returns: subindustry_code, subindustry_name, industry_*, sector_*
    
    def map_batch(tickers: list) -> DataFrame
```

### Rate Limiting

```python
class RateLimiter:
    """Token bucket rate limiter for API calls."""
    
    def __init__(calls_per_second, calls_per_day=None)
    async def acquire()  # Waits if limit reached
```

### Retry Logic

```python
@with_retry(max_retries=3, base_delay=1.0, exponential_backoff=True)
async def fetch_data():
    # Automatically retries on failure
```

### Pipelines

#### Initial Load Pipeline

```
1. Load GICS reference (163 sub-industries) into database
2. Fetch S&P 500 constituents from Wikipedia
3. Map each ticker to GICS sub-industry
4. Create Stock records in database
5. Fetch 2 years of price history using yfinance batch download
6. Store all prices in database
```

#### Daily Price Pipeline

```
1. Get list of active stocks from database
2. Fetch today's prices using yfinance
3. Upsert into StockPrice table
4. Update market_cap in Stock table
```

#### Weekly RS Pipeline (see Section 7)

---

## 6. RS Calculation Engine

### MansfieldRSCalculator

```python
class MansfieldRSCalculator:
    """
    Calculates Mansfield Relative Strength.
    """
    
    def __init__(self, sma_period_weeks: int = 52):
        self.sma_period = sma_period_weeks
    
    def calculate_rs_line(asset_prices, benchmark_prices) -> Series:
        """Step 1: RS_Line = (Asset / Benchmark) × 100"""
        return (asset_prices / benchmark_prices) * 100
    
    def calculate_rs_sma(rs_line) -> Series:
        """Step 2: 52-week SMA of RS Line"""
        return rs_line.rolling(window=52, min_periods=52).mean()
    
    def calculate_mansfield_rs(rs_line, rs_sma) -> Series:
        """Step 3: Mansfield RS = ((RS_Line - SMA) / SMA) × 100"""
        return ((rs_line - rs_sma) / rs_sma) * 100
    
    def calculate_full(asset_prices, benchmark_prices) -> DataFrame:
        """Complete pipeline returning all components"""
```

### SubIndustryAggregator

```python
class SubIndustryAggregator:
    """
    Aggregates individual stock RS into sub-industry level RS.
    Uses market-cap weighting for accurate representation.
    """
    
    def calculate_subindustry_rs(
        stocks_data: dict,      # {ticker: DataFrame}
        benchmark_prices: Series,
        method: str = "market_cap_weighted"  # or "equal_weighted"
    ) -> DataFrame
```

### Percentile Ranking

```python
def calculate_percentile_ranks(rs_values: Series) -> Series:
    """
    Calculate percentile ranks across all sub-industries.
    Returns 0-100 values for color coding.
    
    - Top 33% (percentile >= 67): GREEN (strong)
    - Middle 34% (33 <= percentile < 67): YELLOW (neutral)
    - Bottom 33% (percentile < 33): RED (weak)
    """
    return rs_values.rank(pct=True) * 100
```

---

## 7. Weekly Job Scheduler

### Scheduler Configuration

```python
# APScheduler configuration
scheduler = AsyncIOScheduler(timezone="America/New_York")

# Weekly RS calculation: Saturday 6 AM ET (after Friday close)
scheduler.add_job(
    run_weekly_rs_calculation,
    trigger=CronTrigger(day_of_week="sat", hour=6, minute=0),
    id="weekly_rs_calculation"
)

# Daily price refresh: Mon-Fri 7 PM ET (after market close)
scheduler.add_job(
    run_price_refresh,
    trigger=CronTrigger(day_of_week="mon-fri", hour=19, minute=0),
    id="daily_price_refresh"
)
```

### Weekly RS Job Logic

```
1. Determine last complete week (previous Friday as week_end)
2. Fetch benchmark (SPY) prices for 60+ weeks back
3. For each GICS sub-industry:
   a. Get all active stocks in sub-industry
   b. Fetch price data for each stock
   c. Calculate market-cap weighted aggregate price
   d. Calculate Mansfield RS using calculator
   e. Store RS components for the week
4. Calculate percentile ranks across all sub-industries
5. Update rs_percentile field for each record
6. Log job completion in JobLog table
```

### Week Calculation

```python
def get_last_friday() -> date:
    """Get the most recent Friday (last complete trading week)."""
    today = date.today()
    days_since_friday = (today.weekday() - 4) % 7
    if days_since_friday == 0 and today.weekday() == 4:
        days_since_friday = 7  # Today is Friday, use previous
    return today - timedelta(days=days_since_friday)

def get_week_ranges(months_back: int = 4) -> list:
    """Generate week ranges for the past N months (~17 weeks for 4 months)."""
```

---

## 8. Dashboard Specifications

### Matrix Layout

```
                    WEEKS (X-AXIS) →
         Most Recent                            Oldest
         ┌──────┬──────┬──────┬──────┬──────┬──────┬──────┐
         │ W-01 │ W-02 │ W-03 │ W-04 │ ...  │ W-16 │ W-17 │
    ┌────┼──────┼──────┼──────┼──────┼──────┼──────┼──────┤
S   │Oil │  🟢  │  🟢  │  🟡  │  🟢  │      │  🔴  │  🟡  │
U   │Dril│      │      │      │      │      │      │      │
B   ├────┼──────┼──────┼──────┼──────┼──────┼──────┼──────┤
-   │Gold│  🔴  │  🟡  │  🟢  │  🟢  │      │  🟢  │  🟡  │
I   │Mine│      │      │      │      │      │      │      │
N   ├────┼──────┼──────┼──────┼──────┼──────┼──────┼──────┤
D   │Semi│  🟢  │  🟢  │  🟢  │  🟢  │      │  🟡  │  🔴  │
U   │cond│      │      │      │      │      │      │      │
S   ├────┼──────┼──────┼──────┼──────┼──────┼──────┼──────┤
T   │... │      │      │      │      │      │      │      │
R   ├────┼──────┼──────┼──────┼──────┼──────┼──────┼──────┤
Y   │Soft│  🟡  │  🟡  │  🟢  │  🟢  │      │  🔴  │  🔴  │
    │ware│      │      │      │      │      │      │      │
(Y) └────┴──────┴──────┴──────┴──────┴──────┴──────┴──────┘
↓
163 Sub-Industries
```

**Key Layout Rules:**
- **X-axis (horizontal)**: Weeks — most recent week on LEFT
- **Y-axis (vertical)**: 163 GICS Sub-Industries
- **Week labels on TOP** (xaxis side="top")
- **Industry names on LEFT** with enough margin

### Color Coding (Percentile-Based)

```python
colorscale = [
    [0.00, "#b91c1c"],  # Dark red    (0th percentile)
    [0.20, "#dc2626"],  # Red
    [0.33, "#f97316"],  # Orange      (33rd percentile - weak/neutral boundary)
    [0.45, "#eab308"],  # Yellow
    [0.55, "#facc15"],  # Light yellow
    [0.67, "#84cc16"],  # Lime        (67th percentile - neutral/strong boundary)
    [0.80, "#22c55e"],  # Green
    [1.00, "#15803d"],  # Dark green  (100th percentile)
]
```

| Percentile Range | Color | Interpretation |
|------------------|-------|----------------|
| 67-100 | 🟢 Green | Strong (outperforming) |
| 33-66 | 🟡 Yellow | Neutral (in-line) |
| 0-32 | 🔴 Red | Weak (underperforming) |

### Dashboard Features

1. **Interactive Heatmap**
   - Hover: Show sub-industry name, week, RS percentile, strength label
   - Click: Show detail panel with constituent stocks
   - Zoom/pan: Navigate large matrix

2. **Filters**
   - Sector dropdown (multi-select): Filter by GICS sector
   - Weeks slider: Adjust time range (4-26 weeks)

3. **Sorting Options**
   - Latest RS: Sort by most recent week's percentile
   - RS Change: Sort by 4-week change in percentile
   - Sector: Group by GICS sector
   - Alphabetical: A-Z by sub-industry name

4. **Theme**
   - Dark theme (slate/dark blue background)
   - High contrast colors for readability
   - Bootstrap Darkly theme for UI components

### Plotly Dash Components

```python
# Main layout structure
dbc.Container([
    # Header
    dbc.Row([html.H1("RS Industry Dashboard")]),
    
    # Filters Row
    dbc.Row([
        dbc.Col([dcc.Dropdown(id="sector-filter")], width=4),
        dbc.Col([dcc.RadioItems(id="sort-method")], width=4),
        dbc.Col([dcc.Slider(id="weeks-slider")], width=4),
    ]),
    
    # Heatmap
    dbc.Row([
        dbc.Col([dcc.Graph(id="rs-heatmap", style={"height": "800px"})])
    ]),
    
    # Legend
    dbc.Row([color_legend]),
    
    # Detail Panel (on click)
    dbc.Row([html.Div(id="detail-panel")]),
    
    # Data Store
    dcc.Store(id="rs-data-store"),
])
```

### Heatmap Configuration

```python
fig = go.Figure(data=go.Heatmap(
    z=pivot_df.values,           # RS percentile values
    x=pivot_df.columns,          # Week labels (X-axis)
    y=pivot_df.index,            # Sub-industry names (Y-axis)
    colorscale=colorscale,
    zmin=0,
    zmax=100,
    hovertemplate="%{customdata}<extra></extra>",
    customdata=hover_text,
    xgap=1,
    ygap=1,
))

fig.update_layout(
    xaxis=dict(side="top", title="Weeks"),
    yaxis=dict(autorange="reversed", title="Sub-Industries"),
    paper_bgcolor="#0f172a",
    plot_bgcolor="#1e293b",
    height=max(800, num_industries * 18),
    margin=dict(l=250, r=80, t=100, b=50),
)
```

---

## 9. API Endpoints

### RS Data Endpoints

```
GET /api/rs/matrix
    Query params:
    - weeks: int (default 17)
    - sectors: list[str] (optional filter)
    - sort_by: str (latest|change|alpha)
    
    Response: Matrix data for heatmap

GET /api/rs/subindustry/{code}
    Path params:
    - code: GICS sub-industry code
    
    Response: RS history for specific sub-industry

GET /api/rs/week/{date}
    Path params:
    - date: Week end date (YYYY-MM-DD)
    
    Response: All sub-industry RS for specific week
```

### GICS Endpoints

```
GET /api/gics/sectors
    Response: List of GICS sectors

GET /api/gics/subindustries
    Query params:
    - sector: str (optional filter)
    
    Response: List of sub-industries

GET /api/gics/subindustry/{code}/stocks
    Response: Stocks in sub-industry
```

### Health/Admin Endpoints

```
GET /api/health
    Response: Service health status

GET /api/jobs/status
    Response: Recent job execution logs

POST /api/jobs/trigger/{job_name}
    Trigger manual job execution (admin only)
```

---

## 10. Configuration & Environment

### Environment Variables

```bash
# .env file

# Database
DATABASE_URL=postgresql://rs_user:password@localhost:5432/rs_dashboard

# Redis (for caching)
REDIS_URL=redis://localhost:6379

# Data Ingestion (Optional - for FMP source)
INGESTION_FMP_API_KEY=your_key_here

# App Settings
APP_ENV=development
LOG_LEVEL=INFO

# Scheduler
SCHEDULER_ENABLED=true
```

### Config Class

```python
class Settings(BaseSettings):
    DATABASE_URL: str
    REDIS_URL: str = "redis://localhost:6379"
    
    # Ingestion
    FMP_API_KEY: Optional[str] = None
    YFINANCE_REQUESTS_PER_HOUR: int = 2000
    
    # RS Calculation
    RS_SMA_PERIOD_WEEKS: int = 52
    BENCHMARK_TICKER: str = "SPY"
    
    # Dashboard
    DEFAULT_WEEKS_DISPLAY: int = 17
    MAX_WEEKS_DISPLAY: int = 52
    
    class Config:
        env_file = ".env"
```

---

## 11. Implementation Checklist

### Phase 1: Foundation (Priority: P0)

- [ ] Initialize Python project with Poetry or pip
- [ ] Set up project structure (create directories)
- [ ] Create requirements.txt with all dependencies
- [ ] Set up Docker Compose (PostgreSQL + Redis)
- [ ] Create SQLAlchemy models (all 5 tables)
- [ ] Set up Alembic and create initial migration
- [ ] Create configuration module

### Phase 2: Data Ingestion (Priority: P0)

- [ ] Implement rate limiter utility
- [ ] Implement retry decorator
- [ ] Create yfinance source class
- [ ] Create Wikipedia source class
- [ ] Create GICS mapper
- [ ] Create static GICS reference CSV (163 sub-industries)
- [ ] Implement initial load pipeline
- [ ] Create bootstrap script

### Phase 3: RS Calculation (Priority: P0)

- [ ] Implement MansfieldRSCalculator class
- [ ] Implement SubIndustryAggregator class
- [ ] Implement percentile ranking function
- [ ] Create data service layer
- [ ] Write unit tests for calculations

### Phase 4: Scheduler (Priority: P1)

- [ ] Set up APScheduler
- [ ] Implement weekly RS job
- [ ] Implement daily price refresh job
- [ ] Add job logging
- [ ] Create backfill script for historical data

### Phase 5: Dashboard (Priority: P1)

- [ ] Create Dash app structure
- [ ] Build main layout with filters
- [ ] Implement heatmap callback
- [ ] Add sector filter functionality
- [ ] Add sorting functionality
- [ ] Add weeks slider
- [ ] Implement click-through detail panel
- [ ] Style with dark theme

### Phase 6: API (Priority: P2)

- [ ] Create FastAPI app
- [ ] Implement RS endpoints
- [ ] Implement GICS endpoints
- [ ] Implement health endpoints
- [ ] Mount Dash app on FastAPI
- [ ] Add API documentation

### Phase 7: Deployment (Priority: P2)

- [ ] Create Dockerfile
- [ ] Update docker-compose for production
- [ ] Create .env.example
- [ ] Write README with setup instructions
- [ ] Add error handling and logging
- [ ] Write integration tests

---

## Quick Reference: Key Commands

```bash
# Development Setup
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Database
docker-compose up -d db redis
alembic upgrade head

# Initial Data Load
python -m scripts.bootstrap_data

# Run Application
uvicorn src.main:app --reload --port 8000

# Access Dashboard
# http://localhost:8000/dashboard/

# Manual Job Trigger
python -c "from src.jobs.weekly_rs_job import run_weekly_rs_calculation; import asyncio; asyncio.run(run_weekly_rs_calculation())"
```

---

## Dependencies (requirements.txt)

```
# Web Framework
fastapi>=0.109.0
uvicorn[standard]>=0.27.0

# Database
sqlalchemy>=2.0.25
alembic>=1.13.1
asyncpg>=0.29.0
psycopg2-binary>=2.9.9

# Data Processing
pandas>=2.2.0
numpy>=1.26.0
python-dateutil>=2.8.2

# Data Ingestion
yfinance>=0.2.35
httpx>=0.26.0
lxml>=5.1.0

# Dashboard
dash>=2.14.0
dash-bootstrap-components>=1.5.0
plotly>=5.18.0

# Scheduling
apscheduler>=3.10.4

# Caching
redis>=5.0.1

# Configuration
pydantic>=2.5.0
pydantic-settings>=2.1.0
python-dotenv>=1.0.0

# Testing
pytest>=7.4.0
pytest-asyncio>=0.23.0
```

---

*This specification document provides all the context needed to build the RS Dashboard application. Use it as a reference when prompting an AI assistant to implement specific components.*

