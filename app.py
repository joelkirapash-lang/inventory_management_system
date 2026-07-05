"""
app.py

Flask REST API for the Inventory Management System.

Implements full CRUD over an in-memory inventory "database array",
plus helper routes that integrate with the OpenFoodFacts external API
to search for and import product data.
"""
from flask import Flask, jsonify, request

from data_store import inventory, get_next_id
from external_api import fetch_product_by_barcode, fetch_product_by_name

app = Flask(__name__)


# ---------------------------------------------------------------------
# Helper / informational routes
# ---------------------------------------------------------------------
@app.route("/", methods=["GET"])
def index():
    """Root route - simple welcome message."""
    return jsonify({"message": "Inventory Management API", "status": "running"}), 200


@app.route("/health", methods=["GET"])
def health_check():
    """Helper route to confirm the API is alive and report inventory size."""
    return jsonify({"status": "ok", "items_in_inventory": len(inventory)}), 200


# ---------------------------------------------------------------------
# CRUD routes
# ---------------------------------------------------------------------
@app.route("/inventory", methods=["GET"])
def get_all_items():
    """GET /inventory -> Fetch all inventory items."""
    return jsonify(inventory), 200


@app.route("/inventory/<int:item_id>", methods=["GET"])
def get_item(item_id):
    """GET /inventory/<id> -> Fetch a single inventory item."""
    item = next((i for i in inventory if i["id"] == item_id), None)
    if item is None:
        return jsonify({"error": f"Item with id {item_id} not found"}), 404
    return jsonify(item), 200


@app.route("/inventory", methods=["POST"])
def create_item():
    """POST /inventory -> Add a new inventory item."""
    data = request.get_json(silent=True)
    if not data or not data.get("product_name"):
        return jsonify({"error": "product_name is required"}), 400

    new_item = {
        "id": get_next_id(),
        "product_name": data.get("product_name"),
        "brand": data.get("brand", "Unknown"),
        "barcode": data.get("barcode", ""),
        "quantity": data.get("quantity", 0),
        "price": data.get("price", 0.0),
        "ingredients_text": data.get("ingredients_text", ""),
    }
    inventory.append(new_item)
    return jsonify(new_item), 201


@app.route("/inventory/<int:item_id>", methods=["PATCH"])
def update_item(item_id):
    """PATCH /inventory/<id> -> Update fields of an existing item."""
    item = next((i for i in inventory if i["id"] == item_id), None)
    if item is None:
        return jsonify({"error": f"Item with id {item_id} not found"}), 404

    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "No update data provided"}), 400

    allowed_fields = (
        "product_name",
        "brand",
        "barcode",
        "quantity",
        "price",
        "ingredients_text",
    )
    for key in allowed_fields:
        if key in data:
            item[key] = data[key]

    return jsonify(item), 200


@app.route("/inventory/<int:item_id>", methods=["DELETE"])
def delete_item(item_id):
    """DELETE /inventory/<id> -> Remove an inventory item."""
    item = next((i for i in inventory if i["id"] == item_id), None)
    if item is None:
        return jsonify({"error": f"Item with id {item_id} not found"}), 404

    inventory.remove(item)
    return jsonify({"message": f"Item with id {item_id} deleted"}), 200


# ---------------------------------------------------------------------
# External API integration routes
# ---------------------------------------------------------------------
@app.route("/inventory/search/barcode/<barcode>", methods=["GET"])
def search_by_barcode(barcode):
    """
    Helper route: look up a product on OpenFoodFacts by barcode.
    Does NOT add it to inventory - use the /import route for that.
    """
    result = fetch_product_by_barcode(barcode)
    if result is None:
        return jsonify({"error": "Product not found"}), 404
    return jsonify(result), 200


@app.route("/inventory/search/name/<name>", methods=["GET"])
def search_by_name(name):
    """Helper route: search OpenFoodFacts by product name."""
    results = fetch_product_by_name(name)
    if not results:
        return jsonify({"error": "No products found"}), 404
    return jsonify(results), 200


@app.route("/inventory/import/barcode/<barcode>", methods=["POST"])
def import_by_barcode(barcode):
    """
    Fetch a product from OpenFoodFacts by barcode and add it directly
    to the inventory array. Optional JSON body: {"quantity": .., "price": ..}
    """
    result = fetch_product_by_barcode(barcode)
    if result is None:
        return jsonify({"error": "Product not found in external API"}), 404

    body = request.get_json(silent=True) or {}
    new_item = {
        "id": get_next_id(),
        "product_name": result.get("product_name", "Unknown"),
        "brand": result.get("brands", "Unknown"),
        "barcode": barcode,
        "quantity": body.get("quantity", 0),
        "price": body.get("price", 0.0),
        "ingredients_text": result.get("ingredients_text", ""),
    }
    inventory.append(new_item)
    return jsonify(new_item), 201


if __name__ == "__main__":
    app.run(debug=True)
