"""
test_external_api.py

Unit tests for external_api.py, using unittest.mock to simulate
OpenFoodFacts API responses without making real network calls.
"""
from unittest.mock import patch, MagicMock

from external_api import fetch_product_by_barcode, fetch_product_by_name


def _mock_response(json_data, status_code=200):
    mock_resp = MagicMock()
    mock_resp.status_code = status_code
    mock_resp.json.return_value = json_data
    mock_resp.raise_for_status = MagicMock()
    return mock_resp


@patch("external_api.requests.get")
def test_fetch_product_by_barcode_found(mock_get):
    mock_get.return_value = _mock_response(
        {
            "status": 1,
            "product": {
                "product_name": "Organic Almond Milk",
                "brands": "Silk",
                "ingredients_text": "Filtered water, almonds, cane sugar",
            },
        }
    )
    result = fetch_product_by_barcode("0025293001165")
    assert result is not None
    assert result["product_name"] == "Organic Almond Milk"
    assert result["brands"] == "Silk"
    assert result["barcode"] == "0025293001165"


@patch("external_api.requests.get")
def test_fetch_product_by_barcode_not_found(mock_get):
    mock_get.return_value = _mock_response({"status": 0})
    result = fetch_product_by_barcode("0000000000000")
    assert result is None


@patch("external_api.requests.get")
def test_fetch_product_by_barcode_request_exception(mock_get):
    import requests

    mock_get.side_effect = requests.RequestException("network error")
    result = fetch_product_by_barcode("0025293001165")
    assert result is None


def test_fetch_product_by_barcode_empty_input():
    assert fetch_product_by_barcode("") is None
    assert fetch_product_by_barcode(None) is None


@patch("external_api.requests.get")
def test_fetch_product_by_name_found(mock_get):
    mock_get.return_value = _mock_response(
        {
            "products": [
                {
                    "product_name": "Almond Milk",
                    "brands": "Silk",
                    "ingredients_text": "Almonds, water",
                    "code": "111",
                },
                {
                    "product_name": "Almond Milk Unsweetened",
                    "brands": "Blue Diamond",
                    "ingredients_text": "Almonds, water, salt",
                    "code": "222",
                },
            ]
        }
    )
    results = fetch_product_by_name("almond milk")
    assert len(results) == 2
    assert results[0]["product_name"] == "Almond Milk"
    assert results[1]["barcode"] == "222"


@patch("external_api.requests.get")
def test_fetch_product_by_name_no_results(mock_get):
    mock_get.return_value = _mock_response({"products": []})
    results = fetch_product_by_name("nonexistentproductxyz")
    assert results == []


@patch("external_api.requests.get")
def test_fetch_product_by_name_request_exception(mock_get):
    import requests

    mock_get.side_effect = requests.RequestException("network error")
    results = fetch_product_by_name("almond milk")
    assert results == []


def test_fetch_product_by_name_empty_input():
    assert fetch_product_by_name("") == []
    assert fetch_product_by_name(None) == []
