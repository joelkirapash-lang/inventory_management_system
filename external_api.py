"""
external_api.py

Handles all communication with the OpenFoodFacts external API.
Provides functions to look up a product by barcode or search by name,
normalizing the response into the shape our inventory system expects.

Docs: https://world.openfoodfacts.org/data
"""
import requests

BASE_URL = "https://world.openfoodfacts.org"
REQUEST_TIMEOUT = 10


def fetch_product_by_barcode(barcode):
    """
    Fetch a single product from OpenFoodFacts using its barcode.

    Returns a dict with product details, or None if the product
    was not found or the request failed.
    """
    if not barcode:
        return None

    url = f"{BASE_URL}/api/v2/product/{barcode}.json"
    try:
        response = requests.get(url, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
    except requests.RequestException:
        return None

    data = response.json()
    if data.get("status") != 1:
        return None

    product = data.get("product", {})
    return {
        "product_name": product.get("product_name") or "Unknown",
        "brands": product.get("brands") or "Unknown",
        "ingredients_text": product.get("ingredients_text", ""),
        "barcode": barcode,
    }


def fetch_product_by_name(name, page_size=5):
    """
    Search OpenFoodFacts for products matching a name.

    Returns a list of normalized product dicts (possibly empty).
    """
    if not name:
        return []

    url = f"{BASE_URL}/cgi/search.pl"
    params = {
        "search_terms": name,
        "search_simple": 1,
        "action": "process",
        "json": 1,
        "page_size": page_size,
    }
    try:
        response = requests.get(url, params=params, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
    except requests.RequestException:
        return []

    data = response.json()
    products = data.get("products", [])

    results = []
    for product in products:
        results.append(
            {
                "product_name": product.get("product_name") or "Unknown",
                "brands": product.get("brands") or "Unknown",
                "ingredients_text": product.get("ingredients_text", ""),
                "barcode": product.get("code", ""),
            }
        )
    return results
