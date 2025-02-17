from abc import ABC, abstractmethod
import threading
import time
from django.core.cache import cache
from datetime import datetime, timedelta 
from rest_framework.exceptions import Throttled
from utils.logger import Logger
from utils.config_manager import ConfigManager

logger = Logger().get_logger()
config = ConfigManager()

class RateLimiter(ABC):
    @abstractmethod
    def check_rate_limit(self, request) -> bool:
        pass
    
    @abstractmethod
    def increment(self, key: str) -> None:
        pass
    
    
class InMemoryRateLimiter(RateLimiter):
    def __init__(self, max_requests: int, time_window: int):
        self.max_requests = max_requests
        self.time_window = time_window
        self.cache = {}
        self.cleanup_interval = config.get_settings("RATE_LIMIT_CLEANUP_INTERVAL")
        self._start_cleanup_thread()
        
    def check_rate_limit(self, key: str) -> bool:
        current_time = datetime.now()
        if key not in self.cache:
            return True
        
        requests = [timestamps for timestamps in self.cache[key] if timestamps > current_time - timedelta(seconds=self.time_window)]
        
        return len(requests) < self.max_requests
    
    # Clean up the cache every x seconds
    def _start_cleanup_thread(self):
        def cleanup_task():
            while True:
                self._cleanup_cache()
                time.sleep(self.cleanup_interval)
                
        cleanup_thread = threading.Thread(target=cleanup_task, daemon=True)
        cleanup_thread.start()
        
    # Remove old timestamps from the cache
    def _cleanup_cache(self):
        current_time = datetime.now()
        keys_to_delete = []
        for key, timestamps in self.cache.items():
            # Check if all timestamps for the key are outside the time window
            if all(timestamp < current_time - timedelta(seconds=self.time_window) for timestamp in timestamps):
                keys_to_delete.append(key)
                
        for key in keys_to_delete:
            del self.cache[key]
    
    def increment(self, key: str) -> None:
        current_time = datetime.now()
        if key not in self.cache:
            self.cache[key] = []
        self.cache[key].append(current_time)
        
class RateLimiterFactory:
    @staticmethod
    def create_rate_limiter(limiter_type: str = "memory") -> RateLimiter:
        if limiter_type == "memory":
            return InMemoryRateLimiter(
                max_requests=config.get_settings("RATE_LIMIT_MAX_REQUESTS"),
                time_window=config.get_settings("RATE_LIMIT_TIME_WINDOW"),
            )
        else:
            raise ValueError(f"Invalid rate limiter type: {limiter_type}")
        