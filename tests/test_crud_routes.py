"""
test_crud_routes.py

Unit tests for the CRUD endpoints: GET, POST, PATCH, DELETE.
"""


def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json()["status"] == "ok"


def test_get_all_items(client):
    response = client.get("/inventory")
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) == 2


def test_get_single_item_success(client):
    response = client.get("/inventory/1")
    assert response.status_code == 200
    data = response.get_json()
    assert data["id"] == 1
    assert data["product_name"] == "Organic Almond Milk"


def test_get_single_item_not_found(client):
    response = client.get("/inventory/999")
    assert response.status_code == 404
    assert "error" in response.get_json()


def test_create_item_success(client):
    payload = {
        "product_name": "Sparkling Water",
        "brand": "LaCroix",
        "barcode": "0123456789012",
        "quantity": 20,
        "price": 4.25,
    }
    response = client.post("/inventory", json=payload)
    assert response.status_code == 201
    data = response.get_json()
    assert data["product_name"] == "Sparkling Water"
    assert data["id"] == 3

    # Confirm it actually landed in the inventory list
    get_response = client.get("/inventory")
    assert len(get_response.get_json()) == 3


def test_create_item_missing_product_name(client):
    response = client.post("/inventory", json={"brand": "NoName"})
    assert response.status_code == 400
    assert "error" in response.get_json()


def test_update_item_success(client):
    response = client.patch("/inventory/1", json={"quantity": 5, "price": 2.50})
    assert response.status_code == 200
    data = response.get_json()
    assert data["quantity"] == 5
    assert data["price"] == 2.50
    # Unmodified fields stay the same
    assert data["product_name"] == "Organic Almond Milk"


def test_update_item_not_found(client):
    response = client.patch("/inventory/999", json={"quantity": 5})
    assert response.status_code == 404


def test_update_item_no_body(client):
    response = client.patch("/inventory/1", json=None)
    assert response.status_code == 400


def test_delete_item_success(client):
    response = client.delete("/inventory/1")
    assert response.status_code == 200
    assert "deleted" in response.get_json()["message"]

    get_response = client.get("/inventory/1")
    assert get_response.status_code == 404


def test_delete_item_not_found(client):
    response = client.delete("/inventory/999")
    assert response.status_code == 404
