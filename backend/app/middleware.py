"""Request middleware for logging and error handling."""
import time
import uuid
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from app.logger import logger


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """Middleware to log all HTTP requests with timing and request IDs."""
    
    async def dispatch(self, request: Request, call_next):
        """Process request and log details."""
        # Generate request ID
        request_id = str(uuid.uuid4())[:8]
        request.state.request_id = request_id
        
        # Log request
        logger.info(
            "request_started",
            request_id=request_id,
            method=request.method,
            url=str(request.url),
            client_ip=request.client.host if request.client else "unknown",
        )
        
        start_time = time.time()
        
        # Process request
        try:
            response = await call_next(request)
            process_time = time.time() - start_time
            
            # Log response
            logger.info(
                "request_completed",
                request_id=request_id,
                method=request.method,
                url=str(request.url),
                status_code=response.status_code,
                process_time=f"{process_time:.3f}s",
            )
            
            # Add request ID to response headers
            response.headers["X-Request-ID"] = request_id
            
            return response
            
        except Exception as e:
            process_time = time.time() - start_time
            logger.error(
                "request_failed",
                request_id=request_id,
                method=request.method,
                url=str(request.url),
                error=str(e),
                process_time=f"{process_time:.3f}s",
            )
            raise


class ErrorLoggingMiddleware(BaseHTTPMiddleware):
    """Middleware to log unhandled exceptions."""
    
    async def dispatch(self, request: Request, call_next):
        """Process request and log errors."""
        try:
            return await call_next(request)
        except Exception as e:
            logger.exception(
                "unhandled_exception",
                request_id=getattr(request.state, "request_id", "unknown"),
                method=request.method,
                url=str(request.url),
                error=str(e),
            )
            raise

