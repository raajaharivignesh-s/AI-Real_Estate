import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app

@pytest.mark.asyncio
async def test_get_properties():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/api/v1/properties")
        assert response.status_code == 200
        data = response.json()
        assert "items" in data
        assert "total" in data

@pytest.mark.asyncio
async def test_get_featured_properties():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/api/v1/properties/featured")
        assert response.status_code == 200
        assert isinstance(response.json(), list)
