import pytest
import respx
from app.api_client import fetch_users_batch, fetch_users_total

API_BASE_URL = "https://api.randomdatatools.ru"


@pytest.mark.asyncio
async def test_fetch_users_batch_with_mock():
    mock_users = [
        {
            "FirstName": "Test_firstname_1",
            "LastName": "Test_lastname_1",
            "Email": "test1@test.local",
            "Gender": "male",
            "Phone": "+0 (000) 000-00-01",
            "City": "Test_city_1",
            "Street": "Test_street_1",
            "House": "1"
        },
        {
            "FirstName": "Test_firstname_2",
            "LastName": "Test_lastname_2",
            "Email": "test2@test.local",
            "Gender": "female",
            "Phone": "+0 (000) 000-00-02",
            "City": "Test_city_2",
            "Street": "Test_street_2",
            "House": "2"
        }
    ]
    
    with respx.mock:
        respx.get(f"{API_BASE_URL}/?count=2").respond(json=mock_users)
        
        result = await fetch_users_batch(2)
        
        assert len(result) == 2
        assert result[0]["FirstName"] == "Test_firstname_1"
        assert result[1]["FirstName"] == "Test_firstname_2"
        assert len(respx.calls) == 1


@pytest.mark.asyncio
async def test_fetch_users_total_150_with_mock():
    with respx.mock:
        respx.get(f"{API_BASE_URL}/?count=100").respond(json=[{}] * 100)
        respx.get(f"{API_BASE_URL}/?count=50").respond(json=[{}] * 50)
        
        result = await fetch_users_total(150)
        
        assert len(result) == 150
        assert len(respx.calls) == 2