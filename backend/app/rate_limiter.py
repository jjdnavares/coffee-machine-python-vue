"""Rate limiting configuration for the API."""
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi import Request
from starlette.responses import JSONResponse


def get_remote_address_with_proxy(request: Request) -> str:
    """
    Get client IP address, handling proxy headers.
    """
    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.client.host if request.client else "unknown"


# Create rate limiter with memory-based storage
# For production with Redis, change to: "redis://redis:6379"
limiter = Limiter(
    key_func=get_remote_address_with_proxy,
    default_limits=["100/hour"],
    storage_uri="memory://",
)


async def rate_limit_exceeded_handler(request: Request, exc: RateLimitExceeded) -> JSONResponse:
    """
    Custom handler for rate limit exceeded errors.
    Returns user-friendly JSON response.
    """
    return JSONResponse(
        status_code=429,
        content={
            "success": False,
            "message": "Rate limit exceeded. Please try again later.",
            "error_type": "RateLimitExceeded",
            "details": {
                "retry_after": exc.detail if exc.detail else "1 hour"
            }
        }
    )

