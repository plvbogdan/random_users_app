import pytest
from app.main import app


@pytest.mark.asyncio
async def test_home_page_returns_200(client):
    response = await client.get("/")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_random_user_endpoint_returns_404_when_empty(client):
    response = await client.get("/random")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_user_detail_nonexistent_returns_404(client):
    response = await client.get("/user/99999")
    assert response.status_code == 404