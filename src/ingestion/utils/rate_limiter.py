"""
Rate limiter for API calls.

Implements a token bucket algorithm to control request rates.
"""
import asyncio
import time
from collections import deque
from datetime import datetime, timedelta
from typing import Optional
import logging

logger = logging.getLogger(__name__)


class RateLimitExceeded(Exception):
    """Raised when rate limit is exceeded and cannot wait."""
    pass


class RateLimiter:
    """
    Token bucket rate limiter for API calls.
    
    Supports both per-second and per-day limits.
    Thread-safe for async operations.
    
    Example:
        limiter = RateLimiter(calls_per_second=0.5, calls_per_day=250)
        await limiter.acquire()  # Waits if necessary
        # Make API call
    """
    
    def __init__(
        self,
        calls_per_second: float = 1.0,
        calls_per_day: Optional[int] = None
    ):
        """
        Initialize rate limiter.
        
        Args:
            calls_per_second: Maximum calls per second (can be fractional)
            calls_per_day: Optional daily limit (raises exception when exceeded)
        """
        self.calls_per_second = calls_per_second
        self.calls_per_day = calls_per_day
        self._request_times: deque = deque()
        self._daily_count = 0
        self._daily_reset: Optional[datetime] = None
        self._lock = asyncio.Lock()
    
    async def acquire(self) -> None:
        """
        Acquire permission to make a request.
        
        Waits if necessary to stay within per-second limit.
        Raises RateLimitExceeded if daily limit is reached.
        """
        async with self._lock:
            now = datetime.now()
            
            # Check and reset daily limit
            if self.calls_per_day is not None:
                if self._daily_reset is None or now >= self._daily_reset:
                    self._daily_count = 0
                    # Reset at midnight
                    self._daily_reset = now.replace(
                        hour=0, minute=0, second=0, microsecond=0
                    ) + timedelta(days=1)
                
                if self._daily_count >= self.calls_per_day:
                    wait_seconds = (self._daily_reset - now).total_seconds()
                    logger.warning(
                        f"Daily rate limit of {self.calls_per_day} reached. "
                        f"Resets in {wait_seconds:.0f}s"
                    )
                    raise RateLimitExceeded(
                        f"Daily limit of {self.calls_per_day} reached"
                    )
                
                self._daily_count += 1
            
            # Enforce per-second limit
            min_interval = 1.0 / self.calls_per_second
            if self._request_times:
                last_request = self._request_times[-1]
                elapsed = (now - last_request).total_seconds()
                if elapsed < min_interval:
                    wait_time = min_interval - elapsed
                    logger.debug(f"Rate limiting: waiting {wait_time:.2f}s")
                    await asyncio.sleep(wait_time)
            
            self._request_times.append(datetime.now())
            
            # Keep deque size manageable
            while len(self._request_times) > 100:
                self._request_times.popleft()
    
    def acquire_sync(self) -> None:
        """
        Synchronous version of acquire.
        
        For use in non-async contexts.
        """
        now = datetime.now()
        
        # Check daily limit
        if self.calls_per_day is not None:
            if self._daily_reset is None or now >= self._daily_reset:
                self._daily_count = 0
                self._daily_reset = now.replace(
                    hour=0, minute=0, second=0, microsecond=0
                ) + timedelta(days=1)
            
            if self._daily_count >= self.calls_per_day:
                raise RateLimitExceeded(
                    f"Daily limit of {self.calls_per_day} reached"
                )
            
            self._daily_count += 1
        
        # Enforce per-second limit
        min_interval = 1.0 / self.calls_per_second
        if self._request_times:
            last_request = self._request_times[-1]
            elapsed = (now - last_request).total_seconds()
            if elapsed < min_interval:
                wait_time = min_interval - elapsed
                time.sleep(wait_time)
        
        self._request_times.append(datetime.now())
        
        while len(self._request_times) > 100:
            self._request_times.popleft()
    
    @property
    def remaining_daily(self) -> Optional[int]:
        """Get remaining daily requests, or None if no daily limit."""
        if self.calls_per_day is None:
            return None
        return max(0, self.calls_per_day - self._daily_count)

