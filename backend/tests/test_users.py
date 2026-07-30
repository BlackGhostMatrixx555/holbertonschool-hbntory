def test_admin_can_create_user(client, admin_headers):
    response = client.post("/users", headers=admin_headers, json={
        "username": "marc",
        "password": "Password123!",
        "role": "common",
        "branch_id": 1,
    })
    assert response.status_code == 201
    assert response.json()["username"] == "marc"


def test_common_cannot_list_users(client, employee_headers):
    response = client.get("/users", headers=employee_headers)
    assert response.status_code == 403
