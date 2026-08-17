async def test_login_success(client, user_payload):
    register_payload = user_payload
    await client.post("/auth/register", json=user_payload)

    login_payload = {
        "email": register_payload["email"],
        "password": register_payload["password"],
    }

    response = await client.post("/auth/login", json=login_payload)
    data = response.json()

    assert response.status_code == 200
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "Bearer"
    assert "refresh_token" in response.cookies

async def test_login_wrong_password(client, user_payload):
    user_payload["password"] = "Wrong"

    response = await client.post("/auth/login", json=user_payload)
    assert response.status_code == 401

async def test_login_user_not_found(client, user_payload):
    user_payload["email"] = "test@example.com"

    response = await client.post("/auth/login", json=user_payload)
    assert response.status_code == 401

async def test_login_invalid_email(client, user_payload):
    user_payload["email"] = "test_email.com"

    response = await client.post("/auth/login", json=user_payload)
    assert response.status_code == 422

async def test_login_missing_fields(client, user_payload):
    test_cases = [
        {},
        {"email": user_payload["email"]},
        {"password": user_payload["password"]},
    ]

    for payload in test_cases:
        response = await client.post("/auth/login", json=payload)
        assert response.status_code == 422