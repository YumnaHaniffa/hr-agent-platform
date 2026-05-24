# Create a custom handler that categorizes errors
from fastapi import Request, status
from fastapi.responses import JSONResponse
import logging

# Set up logging to track errors for the developer
logger = logging.getLogger("hr_platform")

async def global_exception_handler(request: Request, exc: Exception):
    """
    Catches any error across the app and returns a polite response.
    """
    # 1. Log the real error for the developer to see in the terminal
    logger.error(f"CRITICAL ERROR: {str(exc)} | Path: {request.url.path}")

    # 2. Determine the message for the User
    message = "Our HR assistant is experiencing a temporary hiccup. Please try again shortly."
    
    # 3. Return a structured JSON response
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "SystemUnavailable",
            "user_message": message,
            "request_id": request.headers.get("X-Request-ID", "unknown")
        }
    )