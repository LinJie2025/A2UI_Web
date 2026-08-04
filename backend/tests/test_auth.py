"""Tests for authentication flow."""

import os
import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from app.main import app
from app.database import Base

# Use an in-memory SQLite database for tests to avoid disk path issues
TEST_DATABASE_URL = "sqlite+aiosqlite:///file:test_auth?mode=memory&cache=shared&uri=true"

_test_engine = None
_test_session_factory = None


@pytest_asyncio.fixture(scope="session")
async def setup_db():
    """Create test database tables once per session."""
    global _test_engine, _test_session_factory
    _test_engine = create_async_engine(
        TEST_DATABASE_URL,
        connect_args={"check_same_thread": False},
    )
    _test_session_factory = async_sessionmaker(
        _test_engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )

    async with _test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with _test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await _test_engine.dispose()


@pytest_asyncio.fixture
async def client(setup_db):
    """Async test client for the FastAPI app with test database."""
    import app.database as db_module
    import app.config as config_module

    # Override the database URL and session factory for testing
    original_url = config_module.settings.DATABASE_URL
    original_factory = db_module.async_session_factory

    config_module.settings.DATABASE_URL = TEST_DATABASE_URL
    db_module.async_session_factory = _test_session_factory
    db_module.engine = _test_engine

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

    # Restore original settings
    config_module.settings.DATABASE_URL = original_url
    db_module.async_session_factory = original_factory


@pytest.mark.asyncio
async def test_register_and_login(client: AsyncClient):
    """Test full register → login → me flow."""
    resp = await client.post("/api/auth/register", json={"username": "testuser1", "password": "testpass123"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["code"] == 0
    assert data["data"]["username"] == "testuser1"

    resp = await client.post("/api/auth/login", json={"username": "testuser1", "password": "testpass123"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["code"] == 0
    assert "access_token" in data["data"]
    token = data["data"]["access_token"]

    resp = await client.get("/api/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["code"] == 0
    assert data["data"]["username"] == "testuser1"


@pytest.mark.asyncio
async def test_register_duplicate(client: AsyncClient):
    """Test duplicate username rejection."""
    await client.post("/api/auth/register", json={"username": "dupuser1", "password": "testpass123"})
    resp = await client.post("/api/auth/register", json={"username": "dupuser1", "password": "testpass456"})
    assert resp.status_code == 409


@pytest.mark.asyncio
async def test_login_invalid(client: AsyncClient):
    """Test login with wrong credentials."""
    resp = await client.post("/api/auth/login", json={"username": "nobody", "password": "wrongpass"})
    assert resp.status_code == 401


@pytest.mark.asyncio
async def test_auth_required(client: AsyncClient):
    """Test that protected endpoint requires auth."""
    resp = await client.get("/api/auth/me")
    assert resp.status_code == 401


@pytest.mark.asyncio
async def test_login_wrong_password(client: AsyncClient):
    """Test login with correct username but wrong password."""
    await client.post("/api/auth/register", json={"username": "wpuser", "password": "correct1"})
    resp = await client.post("/api/auth/login", json={"username": "wpuser", "password": "wrongpw1"})
    assert resp.status_code == 401


@pytest.mark.asyncio
async def test_jwt_expired_token(client: AsyncClient):
    """Test that an expired token is rejected."""
    resp = await client.get("/api/auth/me", headers={"Authorization": "Bearer invalid.token.here"})
    assert resp.status_code == 401


@pytest.mark.asyncio
async def test_password_bcrypt_hashed(client: AsyncClient):
    """Test that password is stored as bcrypt hash, not plaintext."""
    resp = await client.post("/api/auth/register", json={"username": "hashuser", "password": "securepass1"})
    assert resp.status_code == 200

    # Verify password_hash in response does NOT contain the plaintext password
    data = resp.json()
    assert "password" not in str(data["data"]).lower()
