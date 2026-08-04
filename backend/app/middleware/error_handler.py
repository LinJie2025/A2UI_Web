"""Global exception handlers for FastAPI.

Catches all unhandled exceptions and returns a unified JSON response:
{code, data, message}.

Also adds a request_id header to every response for log correlation.
"""

import logging
import uuid
from fastapi import Request, Response
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from app.errors import AppError

logger = logging.getLogger(__name__)


# ── Request ID Middleware ─────────────────────────────────────────────────

class RequestIDMiddleware(BaseHTTPMiddleware):
    """Inject X-Request-ID header into every request/response."""

    async def dispatch(self, request: Request, call_next):
        request_id = request.headers.get("X-Request-ID", str(uuid.uuid4())[:8])
        request.state.request_id = request_id
        response: Response = await call_next(request)
        response.headers["X-Request-ID"] = request_id
        return response


# ── Exception Handlers ────────────────────────────────────────────────────

async def app_error_handler(request: Request, exc: AppError) -> JSONResponse:
    """Handle typed application errors (4xx/5xx)."""
    logger.warning(
        f"[{getattr(request.state, 'request_id', '-')}] "
        f"{exc.code} {exc.status_code}: {exc.message}"
    )
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "code": exc.status_code,
            "data": exc.data,
            "message": exc.message,
        },
    )


async def http_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handle FastAPI HTTPException (from routers)."""
    from fastapi.exceptions import HTTPException
    if isinstance(exc, HTTPException):
        status_code = exc.status_code
        # If detail is a dict with our format, pass it through
        if isinstance(exc.detail, dict) and "message" in exc.detail:
            return JSONResponse(
                status_code=status_code,
                content={
                    "code": status_code,
                    "data": exc.detail.get("data"),
                    "message": exc.detail["message"],
                },
            )
        message = str(exc.detail) if exc.detail else "Unknown error"
        return JSONResponse(
            status_code=status_code,
            content={"code": status_code, "data": None, "message": message},
        )
    # Not an HTTPException — re-raise to general handler
    raise


async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Catch-all for unexpected errors. Logs full traceback, returns generic 500."""
    request_id = getattr(request.state, "request_id", "-")
    logger.error(
        f"[{request_id}] Unhandled exception: {type(exc).__name__}: {exc}",
        exc_info=True,
    )
    return JSONResponse(
        status_code=500,
        content={
            "code": 500,
            "data": None,
            "message": "Internal server error",
        },
    )
