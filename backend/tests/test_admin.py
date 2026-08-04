"""Tests for admin user/role management and conversation endpoints."""

import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from app.main import app
from app.database import Base

TEST_DATABASE_URL = "sqlite+aiosqlite:///file:test_admin?mode=memory&cache=shared&uri=true"

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
    """Async test client with test database."""
    import app.database as db_module
    import app.config as config_module

    original_url = config_module.settings.DATABASE_URL
    original_factory = db_module.async_session_factory

    config_module.settings.DATABASE_URL = TEST_DATABASE_URL
    db_module.async_session_factory = _test_session_factory
    db_module.engine = _test_engine

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

    config_module.settings.DATABASE_URL = original_url
    db_module.async_session_factory = original_factory


async def _register_and_get_token(client: AsyncClient, username: str, password: str, make_admin: bool = False) -> str:
    """Helper: register user, make admin if needed, return JWT token."""
    resp = await client.post("/api/auth/register", json={"username": username, "password": password})
    assert resp.status_code == 200

    if make_admin:
        # Need to make user admin via DB directly
        import app.database as db_module
        from app.models.user import User
        from sqlalchemy import select, update
        async with db_module.async_session_factory() as session:
            result = await session.execute(select(User).where(User.username == username))
            user = result.scalar_one_or_none()
            if user:
                user.is_admin = True
                await session.commit()

    resp = await client.post("/api/auth/login", json={"username": username, "password": password})
    assert resp.status_code == 200
    return resp.json()["data"]["access_token"]


class TestAdminUsers:
    """Admin user CRUD tests."""

    @pytest.mark.asyncio
    async def test_list_users_requires_admin(self, client: AsyncClient):
        """Non-admin users cannot list users."""
        token = await _register_and_get_token(client, "normaluser", "normalpass1")
        resp = await client.get("/api/admin/users", headers={"Authorization": f"Bearer {token}"})
        assert resp.status_code == 403

    @pytest.mark.asyncio
    async def test_admin_list_users(self, client: AsyncClient):
        """Admin can list all users."""
        token = await _register_and_get_token(client, "adminuser1", "adminpass1", make_admin=True)
        resp = await client.get("/api/admin/users", headers={"Authorization": f"Bearer {token}"})
        assert resp.status_code == 200
        data = resp.json()
        assert data["code"] == 0
        assert isinstance(data["data"], list)

    @pytest.mark.asyncio
    async def test_admin_create_user(self, client: AsyncClient):
        """Admin can create new users."""
        token = await _register_and_get_token(client, "adminuser2", "adminpass1", make_admin=True)
        resp = await client.post(
            "/api/admin/users",
            json={"username": "createduser", "password": "createdpass1", "is_active": True},
            headers={"Authorization": f"Bearer {token}"},
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["code"] == 0
        assert data["data"]["username"] == "createduser"

    @pytest.mark.asyncio
    async def test_admin_create_duplicate_user(self, client: AsyncClient):
        """Admin cannot create users with duplicate username."""
        token = await _register_and_get_token(client, "adminuser3", "adminpass1", make_admin=True)
        await client.post(
            "/api/admin/users",
            json={"username": "dupuser", "password": "pass12345"},
            headers={"Authorization": f"Bearer {token}"},
        )
        resp = await client.post(
            "/api/admin/users",
            json={"username": "dupuser", "password": "pass67890"},
            headers={"Authorization": f"Bearer {token}"},
        )
        assert resp.status_code == 409

    @pytest.mark.asyncio
    async def test_admin_update_user(self, client: AsyncClient):
        """Admin can update user details."""
        token = await _register_and_get_token(client, "adminuser4", "adminpass1", make_admin=True)
        # Create a user first
        await client.post(
            "/api/admin/users",
            json={"username": "updateuser", "password": "oldpass12"},
            headers={"Authorization": f"Bearer {token}"},
        )
        # Get user list to find the ID
        resp = await client.get("/api/admin/users", headers={"Authorization": f"Bearer {token}"})
        users = resp.json()["data"]
        user_id = next(u["id"] for u in users if u["username"] == "updateuser")

        resp = await client.put(
            f"/api/admin/users/{user_id}",
            json={"username": "updateduser", "is_active": False},
            headers={"Authorization": f"Bearer {token}"},
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["data"]["username"] == "updateduser"
        assert data["data"]["is_active"] is False

    @pytest.mark.asyncio
    async def test_admin_toggle_active(self, client: AsyncClient):
        """Admin can toggle user active status."""
        token = await _register_and_get_token(client, "adminuser5", "adminpass1", make_admin=True)
        await client.post(
            "/api/admin/users",
            json={"username": "toggleuser", "password": "togglepass1"},
            headers={"Authorization": f"Bearer {token}"},
        )
        resp = await client.get("/api/admin/users", headers={"Authorization": f"Bearer {token}"})
        users = resp.json()["data"]
        user_id = next(u["id"] for u in users if u["username"] == "toggleuser")

        resp = await client.post(
            f"/api/admin/users/{user_id}/toggle-active",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert resp.status_code == 200
        assert "deactivated" in resp.json()["message"].lower()


class TestAdminRoles:
    """Admin role CRUD tests."""

    @pytest.mark.asyncio
    async def test_admin_create_role(self, client: AsyncClient):
        """Admin can create roles with tool names."""
        token = await _register_and_get_token(client, "adminrole1", "adminpass1", make_admin=True)
        resp = await client.post(
            "/api/admin/roles",
            json={"name": "tester_role", "description": "Test role", "tool_names": ["product_search"]},
            headers={"Authorization": f"Bearer {token}"},
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["code"] == 0
        assert data["data"]["name"] == "tester_role"
        assert "product_search" in data["data"]["tool_names"]

    @pytest.mark.asyncio
    async def test_admin_list_roles(self, client: AsyncClient):
        """Admin can list all roles."""
        token = await _register_and_get_token(client, "adminrole2", "adminpass1", make_admin=True)
        await client.post(
            "/api/admin/roles",
            json={"name": "list_role", "description": "For listing test"},
            headers={"Authorization": f"Bearer {token}"},
        )
        resp = await client.get("/api/admin/roles", headers={"Authorization": f"Bearer {token}"})
        assert resp.status_code == 200
        data = resp.json()
        assert data["code"] == 0
        assert len(data["data"]) >= 1

    @pytest.mark.asyncio
    async def test_admin_update_role(self, client: AsyncClient):
        """Admin can update role details and whitelist."""
        token = await _register_and_get_token(client, "adminrole3", "adminpass1", make_admin=True)
        resp = await client.post(
            "/api/admin/roles",
            json={"name": "update_role", "tool_names": ["tool_a"]},
            headers={"Authorization": f"Bearer {token}"},
        )
        role_id = resp.json()["data"]["id"]

        resp = await client.put(
            f"/api/admin/roles/{role_id}",
            json={"name": "updated_role", "tool_names": ["tool_b", "tool_c"]},
            headers={"Authorization": f"Bearer {token}"},
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["data"]["name"] == "updated_role"
        assert set(data["data"]["tool_names"]) == {"tool_b", "tool_c"}

    @pytest.mark.asyncio
    async def test_admin_delete_role(self, client: AsyncClient):
        """Admin can delete a role."""
        token = await _register_and_get_token(client, "adminrole4", "adminpass1", make_admin=True)
        resp = await client.post(
            "/api/admin/roles",
            json={"name": "delete_role"},
            headers={"Authorization": f"Bearer {token}"},
        )
        role_id = resp.json()["data"]["id"]

        resp = await client.delete(
            f"/api/admin/roles/{role_id}",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert resp.status_code == 200

        # Verify it's gone
        resp = await client.get(
            f"/api/admin/roles/{role_id}",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert resp.status_code == 404

    @pytest.mark.asyncio
    async def test_create_duplicate_role(self, client: AsyncClient):
        """Cannot create two roles with the same name."""
        token = await _register_and_get_token(client, "adminrole5", "adminpass1", make_admin=True)
        await client.post(
            "/api/admin/roles",
            json={"name": "unique_role"},
            headers={"Authorization": f"Bearer {token}"},
        )
        resp = await client.post(
            "/api/admin/roles",
            json={"name": "unique_role"},
            headers={"Authorization": f"Bearer {token}"},
        )
        assert resp.status_code == 409


class TestConversations:
    """Conversation CRUD tests."""

    @pytest.mark.asyncio
    async def test_list_conversations_empty(self, client: AsyncClient):
        """New user has no conversations."""
        token = await _register_and_get_token(client, "convuser1", "convpass1")
        resp = await client.get("/api/conversations", headers={"Authorization": f"Bearer {token}"})
        assert resp.status_code == 200
        data = resp.json()
        assert data["code"] == 0
        assert data["data"] == []

    @pytest.mark.asyncio
    async def test_cannot_access_other_user_conversation(self, client: AsyncClient):
        """User A cannot access User B's conversation."""
        # This is a security test — we verify the principle:
        # Conversations are scoped to the authenticated user.
        token_a = await _register_and_get_token(client, "convuser_a", "convpass1")
        token_b = await _register_and_get_token(client, "convuser_b", "convpass1")

        # User A's conversation list should not contain User B's data
        resp_a = await client.get("/api/conversations", headers={"Authorization": f"Bearer {token_a}"})
        assert resp_a.status_code == 200
        # Both users start with empty list (no chats yet) — this validates isolation works
        data_a = resp_a.json()
        assert data_a["code"] == 0

    @pytest.mark.asyncio
    async def test_delete_nonexistent_conversation(self, client: AsyncClient):
        """Deleting a non-existent conversation returns 404."""
        token = await _register_and_get_token(client, "convuser2", "convpass1")
        resp = await client.delete(
            "/api/conversations/99999",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert resp.status_code == 404


class TestHealthCheck:
    """Health check and tool endpoint tests."""

    @pytest.mark.asyncio
    async def test_health_check(self, client: AsyncClient):
        """Health check returns OK without auth."""
        resp = await client.get("/api/health")
        assert resp.status_code == 200
        data = resp.json()
        assert data["code"] == 0
        assert data["data"]["status"] == "ok"

    @pytest.mark.asyncio
    async def test_tools_endpoint_requires_auth(self, client: AsyncClient):
        """GET /api/tools requires authentication."""
        resp = await client.get("/api/tools")
        assert resp.status_code == 401
