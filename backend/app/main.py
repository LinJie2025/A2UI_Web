"""FastAPI application entry point.

Startup: pull global MCP tool list and cache in memory.
Shutdown: dispose database engine.
"""

import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import HTTPException
from app.config import settings
from app.database import engine, Base, async_session_factory
from app.services import mcp_client
from app.errors import AppError
from app.middleware.error_handler import (
    RequestIDMiddleware,
    app_error_handler,
    http_exception_handler,
    general_exception_handler,
)

# In-memory cache for global tool definitions loaded at startup
global_tools_cache: list[dict] = []

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan: create tables on startup, dispose engine on shutdown."""
    # Startup
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Database tables created (if not exist).")

    # Pull global tool list from Odoo MCP
    global global_tools_cache
    try:
        client = mcp_client.MCPClient(
            base_url=settings.ODOO_MCP_URL,
            token=settings.ODOO_MCP_DEFAULT_TOKEN,
        )
        result = await client.list_tools()
        global_tools_cache.clear()
        global_tools_cache.extend(result)
        logger.info(f"Loaded {len(global_tools_cache)} tools from MCP at startup.")
    except Exception as e:
        logger.warning(f"Failed to load tools from MCP at startup: {e}. Will retry per-request.")
        global_tools_cache = []

    yield

    # Shutdown
    await engine.dispose()
    logger.info("Database engine disposed.")


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    lifespan=lifespan,
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[str(origin) for origin in settings.CORS_ORIGINS],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request ID — must be after CORS
app.add_middleware(RequestIDMiddleware)

# Global exception handlers
app.add_exception_handler(AppError, app_error_handler)
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)

# ── Import and register API routers ──
from app.api.auth import router as auth_router
from app.api.chat import router as chat_router
from app.api.tools import router as tools_router
from app.api.users import router as users_router
from app.api.roles import router as roles_router
from app.api.conversations import router as conversations_router
from app.api.a2ui import router as a2ui_router

app.include_router(auth_router, prefix="/api")
app.include_router(chat_router, prefix="/api")
app.include_router(tools_router, prefix="/api")
app.include_router(users_router, prefix="/api")
app.include_router(roles_router, prefix="/api")
app.include_router(conversations_router, prefix="/api")
app.include_router(a2ui_router, prefix="/api")


@app.get("/api/health")
async def health_check():
    """Health check endpoint."""
    return {"code": 0, "data": {"status": "ok", "tools_loaded": len(global_tools_cache)}, "message": "success"}


# ── Error test endpoints (development only) ──────────────────────────────
from app.errors import NotFoundError, ConflictError, ValidationError, UnauthorizedError, ForbiddenError, ServiceUnavailableError

@app.get("/api/test-error/{error_type}")
async def test_error(error_type: str):
    """Trigger a specific error type to test frontend error display.

    Usage:
      /api/test-error/not-found     → 404 + NotFoundError
      /api/test-error/conflict      → 409 + ConflictError
      /api/test-error/validation    → 422 + ValidationError
      /api/test-error/unauthorized  → 401 + UnauthorizedError
      /api/test-error/forbidden     → 403 + ForbiddenError
      /api/test-error/service       → 503 + ServiceUnavailableError
      /api/test-error/crash         → 500 + unexpected Exception
    """
    error_map = {
        "not-found": lambda: (_ for _ in ()).throw(NotFoundError("Contact", 42)),
        "conflict": lambda: (_ for _ in ()).throw(ConflictError("Email already exists: test@example.com")),
        "validation": lambda: (_ for _ in ()).throw(ValidationError("Name is required", data={"field": "name"})),
        "unauthorized": lambda: (_ for _ in ()).throw(UnauthorizedError()),
        "forbidden": lambda: (_ for _ in ()).throw(ForbiddenError()),
        "service": lambda: (_ for _ in ()).throw(ServiceUnavailableError("Odoo MCP", "Connection refused")),
        "crash": lambda: 1 / 0,
    }
    trigger = error_map.get(error_type)
    if trigger is None:
        return {"code": 0, "data": {"available": list(error_map.keys())}, "message": "Use one of these error types"}
    trigger()  # Will raise the error, caught by exception handlers
