"""Typed error hierarchy for the A2UI backend.

All application errors inherit from AppError, which ensures a consistent
response format: {code, data, message}.
"""


class AppError(Exception):
    """Base application error with HTTP status code.

    Attributes:
        message: Human-readable error message.
        code: Machine-readable error code (e.g. "NOT_FOUND").
        status_code: HTTP status code.
        data: Optional payload (e.g. validation error details).
    """

    def __init__(
        self,
        message: str,
        code: str = "INTERNAL_ERROR",
        status_code: int = 500,
        data: dict | None = None,
    ):
        self.message = message
        self.code = code
        self.status_code = status_code
        self.data = data
        super().__init__(message)


# ── Client errors (4xx) ─────────────────────────────────────────────────

class NotFoundError(AppError):
    def __init__(self, resource: str, identifier: str | int):
        super().__init__(
            message=f"{resource} not found: {identifier}",
            code="NOT_FOUND",
            status_code=404,
        )


class ConflictError(AppError):
    def __init__(self, message: str):
        super().__init__(message=message, code="CONFLICT", status_code=409)


class ValidationError(AppError):
    def __init__(self, message: str, data: dict | None = None):
        super().__init__(
            message=message, code="VALIDATION_ERROR", status_code=422, data=data
        )


class UnauthorizedError(AppError):
    def __init__(self, message: str = "Authentication required"):
        super().__init__(
            message=message, code="UNAUTHORIZED", status_code=401
        )


class ForbiddenError(AppError):
    def __init__(self, message: str = "Permission denied"):
        super().__init__(message=message, code="FORBIDDEN", status_code=403)


# ── Server errors (5xx) ─────────────────────────────────────────────────

class ServiceUnavailableError(AppError):
    def __init__(self, service: str, detail: str = ""):
        msg = f"Service unavailable: {service}"
        if detail:
            msg += f" — {detail}"
        super().__init__(message=msg, code="SERVICE_UNAVAILABLE", status_code=503)
