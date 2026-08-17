async def test_get_me_success(auth_client):
    response = await auth_client.get("/users/me")
    data = response.json()

    assert response.status_code == 200

    assert "email" in data
    assert "username" in data
    assert "id" in data

async def test_get_me_without_token(client):
    response = await client.get("/users/me")
    assert response.status_code == 401

async def test_get_me_with_invalid_token(client):
    headers = {"Authorization": "Bearer invalid_token"}
    response = await client.get("/users/me", headers=headers)
    assert response.status_code == 401

async def test_update_me_success(auth_client):
    update_data = {"username": "new_username"}

    response = await auth_client.patch("/users/me", json=update_data)
    data = response.json()

    assert response.status_code == 200
    assert data["username"] == "new_username"

async def test_update_me_username_and_description(auth_client):
    update_data = {"username": "updated_user", "description": "Updated description"}
    response = await auth_client.patch("/users/me", json=update_data)
    data = response.json()

    assert response.status_code == 200
    assert data["username"] == "updated_user"
    assert data["description"] == "Updated description"

async def test_update_me_without_token(client):
    response = await client.patch("/users/me", json={"username": "new"})
    assert response.status_code == 401

async def test_change_password_success(auth_client, registered_user, client):
    password_data = {"current_password": registered_user["password"], "new_password": "NewPassword"}

    response = await auth_client.patch("/users/me/change-password", json=password_data)
    assert response.status_code == 200

    login_response = await client.post("/auth/login", json={"email": registered_user["email"], "password": "NewPassword"})
    assert login_response.status_code == 200

async def test_change_password_wrong_old_password(auth_client):
    password_data = {"current_password": "WrongOldPassword", "new_password": "NewPassword"}

    response = await auth_client.patch("/users/me/change-password", json=password_data)
    assert response.status_code == 401

async def test_change_password_weak_new_password(auth_client, registered_user):
    password_data = {"current_password": registered_user["password"], "new_password": "123"}

    response = await auth_client.patch("/users/me/change-password", json=password_data)
    assert response.status_code == 422

async def test_change_password_without_token(client):
    password_data = {"current_password": "WrongOldPassword", "new_password": "NewPassword"}

    response = await client.patch("/users/me/change-password", json=password_data)
    assert response.status_code == 401

async def test_delete_me_success(auth_client, registered_user, client):
    response = await auth_client.delete("/users/me")
    assert response.status_code == 200

    login_response = await client.post("/auth/login", json={"email": registered_user["email"], "password": registered_user["password"]})
    assert login_response.status_code == 401

async def test_delete_me_without_token(client):
    response = await client.delete("/users/me")
    assert response.status_code == 401