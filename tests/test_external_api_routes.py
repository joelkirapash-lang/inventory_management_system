"""
test_external_api_routes.py

Tests for the Flask routes that integrate with OpenFoodFacts:
/inventory/search/barcode/<barcode>
/inventory/search/name/<name>
/inventory/import/barcode/<barcode>

The external API calls themselves are mocked so tests run offline
and deterministically.
"""
from unittest.mock import patch


@patch("app.fetch_product_by_barcode")
def test_search_by_barcode_found(mock_fetch, client):
    mock_fetch.return_value = {
        "product_name": "Peanut Butter",
        "brands": "Jif",
        "ingredients_text": "Peanuts, sugar, salt",
        "barcode": "999",
    }
    response = client.get("/inventory/search/barcode/999")
    assert response.status_code == 200
    data = response.get_json()
    assert data["product_name"] == "Peanut Butter"


@patch("app.fetch_product_by_barcode")
def test_search_by_barcode_not_found(mock_fetch, client):
    mock_fetch.return_value = None
    response = client.get("/inventory/search/barcode/000")
    assert response.status_code == 404


@patch("app.fetch_product_by_name")
def test_search_by_name_found(mock_fetch, client):
    mock_fetch.return_value = [
        {"product_name": "Peanut Butter", "brands": "Jif", "barcode": "999"}
    ]
    response = client.get("/inventory/search/name/peanut")
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 1


@patch("app.fetch_product_by_name")
def test_search_by_name_not_found(mock_fetch, client):
    mock_fetch.return_value = []
    response = client.get("/inventory/search/name/xyzabc")
    assert response.status_code == 404


@patch("app.fetch_product_by_barcode")
def test_import_by_barcode_success(mock_fetch, client):
    mock_fetch.return_value = {
        "product_name": "Peanut Butter",
        "brands": "Jif",
        "ingredients_text": "Peanuts, sugar, salt",
        "barcode": "999",
    }
    response = client.post(
        "/inventory/import/barcode/999", json={"quantity": 10, "price": 3.50}
    )
    assert response.status_code == 201
    data = response.get_json()
    assert data["product_name"] == "Peanut Butter"
    assert data["quantity"] == 10
    assert data["price"] == 3.50

    # Confirm it was actually appended to the inventory array
    get_response = client.get("/inventory")
    assert len(get_response.get_json()) == 3


@patch("app.fetch_product_by_barcode")
def test_import_by_barcode_not_found(mock_fetch, client):
    mock_fetch.return_value = None
    response = client.post("/inventory/import/barcode/000")
    assert response.status_code == 404

    # Inventory should be unchanged
    get_response = client.get("/inventory")
    assert len(get_response.get_json()) == 2
