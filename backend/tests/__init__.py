"""Basic tests for authentication endpoints."""


async def test_register_and_login(client):
    """Test full register → login → me flow."""
    # Register
    resp = await client.post("/api/auth/register", json={"username": "testuser", "password": "testpass123"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["code"] == 0
    assert data["data"]["username"] == "testuser"

    # Login
    resp = await client.post("/api/auth/login", json={"username": "testuser", "password": "testpass123"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["code"] == 0
    assert "access_token" in data["data"]
    token = data["data"]["access_token"]

    # Me
    resp = await client.get("/api/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["code"] == 0
    assert data["data"]["username"] == "testuser"


async def test_register_duplicate(client):
    """Test duplicate username rejection."""
    await client.post("/api/auth/register", json={"username": "dupuser", "password": "testpass123"})
    resp = await client.post("/api/auth/register", json={"username": "dupuser", "password": "testpass456"})
    assert resp.status_code == 409


async def test_login_invalid(client):
    """Test login with wrong credentials."""
    resp = await client.post("/api/auth/login", json={"username": "nobody", "password": "wrong"})
    assert resp.status_code == 401


async def test_auth_required(client):
    """Test that protected endpoint requires auth."""
    resp = await client.get("/api/auth/me")
    assert resp.status_code == 401
