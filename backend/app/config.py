"""Application configuration via pydantic-settings."""

from typing import List
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables / .env file."""

    # ── Application ──
    APP_NAME: str = "A2UI Web"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False

    # ── Security ──
    SECRET_KEY: str = "change-me-to-a-random-64-char-string"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_HOURS: int = 24

    # ── Database ──
    DATABASE_URL: str = "sqlite+aiosqlite:///./data/a2ui.db"

    # ── LLM ──
    LLM_API_KEY: str = "sk-placeholder"
    LLM_BASE_URL: str = "https://api.deepseek.com"
    LLM_MODEL: str = "deepseek-chat"
    LLM_MAX_TOKENS: int = 4096

    # ── Odoo MCP ──
    ODOO_MCP_URL: str = "http://localhost:8069"
    ODOO_MCP_DEFAULT_TOKEN: str = "default-mcp-token"

    # ── CORS ──
    CORS_ORIGINS: List[str] = ["http://localhost", "http://localhost:80", "http://127.0.0.1"]

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8", "case_sensitive": True}


settings = Settings()
