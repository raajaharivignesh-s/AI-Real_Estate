import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app

@pytest.mark.asyncio
async def test_unauthorized_operations():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/api/v1/visits")
        assert response.status_code == 401
        
        response = await ac.get("/api/v1/bookings")
        assert response.status_code == 401
        
        response = await ac.get("/api/v1/support/requests")
        assert response.status_code == 401
