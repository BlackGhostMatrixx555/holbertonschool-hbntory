def test_login_and_me(client):
    response = client.post("/auth/login", json={"username": "admin", "password": "Admin123!"})
    assert response.status_code == 200
    token = response.json()["access_token"]
    me = client.get("/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert me.status_code == 200
    assert me.json()["username"] == "admin"


def test_invalid_login(client):
    response = client.post("/auth/login", json={"username": "admin", "password": "wrongpass"})
    assert response.status_code == 401
