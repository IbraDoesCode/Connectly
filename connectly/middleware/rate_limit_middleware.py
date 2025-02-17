from django.http import JsonResponse
from rest_framework import status
from utils.rate_limiter import RateLimiterFactory
from utils.logger import Logger
from utils.response_factory import ResponseFactory

logger = Logger().get_logger()

class RateLimitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.rate_limiter = RateLimiterFactory.create_rate_limiter("memory")
        
    def __call__(self, request):
        # Skip rate limiting for certain paths (optional)
        if request.path.startswith("/admin/"):
            return self.get_response(request)
        
        # Create a unique key for the client
        client_ip = request.META.get("REMOTE_ADDR")
        key = f"rate_limit:{client_ip}"
        
        # Check rate limit
        if not self.rate_limiter.check_rate_limit(key):
            logger.warning(f"Rate limit exceeded for IP: {client_ip}")
            return ResponseFactory.too_many_requests("Rate limit exceeded. Try again later.")
        
        # Increment rate limit if the request is allowed
        self.rate_limiter.increment(key)
        
        # Let the request pass
        return self.get_response(request)