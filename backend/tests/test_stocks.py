def test_common_can_add_and_remove_stock(client, employee_headers):
    add = client.post("/stocks/add", headers=employee_headers, json={"product_id": "HB-LAP-1001", "quantity": 8})
    assert add.status_code == 200
    assert add.json()["quantity"] == 8
    assert add.json()["branch_name"] == "Paris"
    remove = client.post("/stocks/remove", headers=employee_headers, json={"product_id": "HB-LAP-1001", "quantity": 3})
    assert remove.status_code == 200
    assert remove.json()["quantity"] == 5


def test_cannot_create_negative_stock(client, employee_headers):
    client.post("/stocks/add", headers=employee_headers, json={"product_id": "HB-KEY-2003", "quantity": 2})
    response = client.post("/stocks/remove", headers=employee_headers, json={"product_id": "HB-KEY-2003", "quantity": 3})
    assert response.status_code == 409

