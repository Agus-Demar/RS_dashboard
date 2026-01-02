"""
Application configuration using Pydantic Settings.
"""
from pathlib import Path
from typing import Optional

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Paths
    BASE_DIR: Path = Path(__file__).parent.parent
    DATA_DIR: Path = BASE_DIR / "data"
    DATABASE_PATH: Path = DATA_DIR / "rs_dashboard.db"
    
    # Database
    DATABASE_URL: Optional[str] = None
    
    @property
    def db_url(self) -> str:
        """Get database URL, defaulting to SQLite."""
        if self.DATABASE_URL:
            return self.DATABASE_URL
        return f"sqlite:///{self.DATABASE_PATH}"
    
    # RS Calculation
    RS_SMA_PERIOD_WEEKS: int = 52
    BENCHMARK_TICKER: str = "SPY"
    PRICE_HISTORY_YEARS: int = 2
    
    # Dashboard
    DEFAULT_WEEKS_DISPLAY: int = 17
    MAX_WEEKS_DISPLAY: int = 52
    
    # Rate Limiting
    YFINANCE_REQUESTS_PER_HOUR: int = 2000
    
    # Scheduler
    SCHEDULER_ENABLED: bool = True
    SCHEDULER_TIMEZONE: str = "America/New_York"
    
    # App Settings
    APP_ENV: str = "development"
    LOG_LEVEL: str = "INFO"
    DEBUG: bool = True
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"


# Global settings instance
settings = Settings()

# Ensure data directory exists
settings.DATA_DIR.mkdir(parents=True, exist_ok=True)

