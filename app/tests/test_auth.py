from httpx import AsyncClient
import pytest
import uuid


@pytest.mark.asyncio
async def test_register_and_login(client):
    email = f"test_{uuid.uuid4().hex}@gmail.com"

    response = await client.post("/auth/register", json={
        "email": email,
        "password": "123456"
    })
    print(response.status_code, response.json())
    assert response.status_code in [200, 201]

    response = await client.post("/auth/login", json={
        "email": email,
        "password": "123456"
    })
    print(response.status_code, response.json())
    assert response.status_code == 200
    assert "access_token" in response.json()

