import pytest
from datetime import datetime, timedelta
from utils.rate_limiter import RateLimiterFactory
from utils.config_manager import ConfigManager

@pytest.mark.django_db
def test_initial_request_allowed(rate_limiter):
    key = "test_ip"

    assert rate_limiter.check_rate_limit(key) is True

@pytest.mark.django_db
def test_under_limit_requests_allowed(rate_limiter):
    key = "test_ip"

    for _ in range(1):  # One less than limit
        rate_limiter.increment(key)
    assert rate_limiter.check_rate_limit(key) is True

@pytest.mark.django_db
def test_exceeding_limit_blocked(rate_limiter):
    key = "test_ip"

    for _ in range(5):  # Hit the limit
        rate_limiter.increment(key)
    assert rate_limiter.check_rate_limit(key) is False

@pytest.mark.django_db
def test_limit_reset_after_window(monkeypatch, rate_limiter):
    key = "test_ip"

    # Set up initial state
    for _ in range(5):
        rate_limiter.increment(key)
    assert rate_limiter.check_rate_limit(key) is False

    # Mock time to be after window
    future_time = datetime.now() + timedelta(seconds=1)  # Correct time delta
    monkeypatch.setattr('utils.rate_limiter.datetime', 
                       type('MockDateTime', (), {'now': lambda: future_time}))

    # Should allow requests again
    assert rate_limiter.check_rate_limit(key) is True


@pytest.mark.django_db
def test_multiple_keys_independent(rate_limiter):
    key1 = "test_ip_1"
    key2 = "test_ip_2"

    # Max out first key
    for _ in range(5):
        rate_limiter.increment(key1)

    # Second key should still work
    assert rate_limiter.check_rate_limit(key1) is False
    assert rate_limiter.check_rate_limit(key2) is True

@pytest.mark.django_db
def test_cleanup_removes_old_entries(monkeypatch, rate_limiter):
    key = "test_ip"

    # Add some requests
    rate_limiter.increment(key)
    
    # Mock time to be after cleanup interval and window
    future_time = datetime.now() + timedelta(seconds=2) #Added 1 more second to make sure it is outside the window
    monkeypatch.setattr('utils.rate_limiter.datetime', 
                       type('MockDateTime', (), {'now': lambda: future_time}))

    # Force cleanup
    rate_limiter._cleanup_cache()
    
    # Cache should be clean
    assert len(rate_limiter.cache) == 0