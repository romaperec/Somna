import pytest

async def test_register_success(client, user_payload):
    response = await client.post("/auth/register", json=user_payload)
    data = response.json()

    assert response.status_code == 201
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "Bearer"
    assert "refresh_token" in response.cookies

async def test_register_duplicate_email(client, user_payload):
    response1 = await client.post("/auth/register", json=user_payload)
    assert response1.status_code == 201

    response2 = await client.post("/auth/register", json=user_payload)
    assert response2.status_code == 409

@pytest.mark.parametrize(
    "invalid_password",
    [
        "test",
        "1111111",
        "NoDigits!",
        "only_lower1!",
        "ONLY_UPPER1!",
        "NoSpecial123",
    ],
)
async def test_register_invalid_password(client, user_payload, invalid_password):
    user_payload["password"] = invalid_password

    response = await client.post("/auth/register", json=user_payload)
    assert response.status_code == 422

async def test_register_invalid_email(client, user_payload):
    user_payload["email"] = "test_email.com"

    response = await client.post("/auth/register", json=user_payload)
    assert response.status_code == 422

async def test_register_does_not_return_password(client, user_payload):
    response = await client.post("/auth/register", json=user_payload)
    data = response.json()

    assert "password" not in data
    assert "hashed_password" not in data

async def test_register_access_token_works(client, user_payload):
    response = await client.post("/auth/register", json=user_payload)
    data = response.json()

    headers = {"Authorization": f"Bearer {data['access_token']}"}

    me_response = await client.get("/users/me", headers=headers)
    assert me_response.status_code == 200