import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app
import uuid

@pytest.mark.asyncio
async def test_auth_flow():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        # Register
        unique_id = uuid.uuid4().hex[:8]
        register_data = {
            "email": f"testauth_{unique_id}@demo.com",
            "password": "password123",
            "full_name": "Test Auth"
        }
        res_register = await ac.post("/api/v1/auth/register", json=register_data)
        assert res_register.status_code == 200
        assert res_register.json()["email"] == register_data["email"]
        
        # Login
        login_data = {
            "email": register_data["email"],
            "password": "password123"
        }
        res_login = await ac.post("/api/v1/auth/login", json=login_data)
        assert res_login.status_code == 200
        token = res_login.json()["access_token"]
        
        # Get Me
        res_me = await ac.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {token}"})
        assert res_me.status_code == 200
        assert res_me.json()["email"] == register_data["email"]
