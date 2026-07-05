"""
cli.py

Command-line interface for the Inventory Management System.
Communicates with the Flask API over HTTP using the `requests` library.

Run the Flask server first (`python app.py`), then run this file
(`python cli.py`) in a separate terminal.
"""
import requests

API_URL = "http://127.0.0.1:5000"


def _is_number(value):
    try:
        float(value)
        return True
    except (TypeError, ValueError):
        return False


def print_item(item):
    """Pretty-print a single inventory item."""
    print("-" * 40)
    print(f"ID: {item.get('id', 'N/A')}")
    print(f"Product: {item.get('product_name', 'N/A')}")
    print(f"Brand: {item.get('brand', item.get('brands', 'N/A'))}")
    print(f"Barcode: {item.get('barcode', 'N/A')}")
    print(f"Quantity: {item.get('quantity', 'N/A')}")
    print(f"Price: {item.get('price', 'N/A')}")
    print("-" * 40)


def view_all_items():
    """Fetch and display every item currently in inventory."""
    response = requests.get(f"{API_URL}/inventory")
    if response.status_code == 200:
        items = response.json()
        if not items:
            print("Inventory is empty.")
            return
        for item in items:
            print_item(item)
    else:
        print("Failed to fetch inventory.")


def view_single_item():
    """Prompt for an ID and display that single item."""
    item_id = input("Enter item ID: ").strip()
    if not item_id.isdigit():
        print("Invalid ID.")
        return
    response = requests.get(f"{API_URL}/inventory/{item_id}")
    if response.status_code == 200:
        print_item(response.json())
    else:
        print(response.json().get("error", "Item not found."))


def add_item():
    """Prompt for details of a new item and POST it to the API."""
    product_name = input("Product name: ").strip()
    brand = input("Brand: ").strip()
    barcode = input("Barcode (optional): ").strip()
    quantity = input("Quantity: ").strip()
    price = input("Price: ").strip()

    payload = {
        "product_name": product_name,
        "brand": brand,
        "barcode": barcode,
        "quantity": int(quantity) if quantity.isdigit() else 0,
        "price": float(price) if _is_number(price) else 0.0,
    }
    response = requests.post(f"{API_URL}/inventory", json=payload)
    if response.status_code == 201:
        print("Item added successfully:")
        print_item(response.json())
    else:
        print(response.json().get("error", "Failed to add item."))


def update_item():
    """Prompt for an ID and new price/quantity, then PATCH the item."""
    item_id = input("Enter item ID to update: ").strip()
    if not item_id.isdigit():
        print("Invalid ID.")
        return

    print("Leave a field blank to keep its current value.")
    quantity = input("New quantity: ").strip()
    price = input("New price: ").strip()

    payload = {}
    if quantity:
        payload["quantity"] = int(quantity) if quantity.isdigit() else 0
    if price:
        payload["price"] = float(price) if _is_number(price) else 0.0

    if not payload:
        print("No changes provided.")
        return

    response = requests.patch(f"{API_URL}/inventory/{item_id}", json=payload)
    if response.status_code == 200:
        print("Item updated successfully:")
        print_item(response.json())
    else:
        print(response.json().get("error", "Failed to update item."))


def delete_item():
    """Prompt for an ID and DELETE that item."""
    item_id = input("Enter item ID to delete: ").strip()
    if not item_id.isdigit():
        print("Invalid ID.")
        return
    response = requests.delete(f"{API_URL}/inventory/{item_id}")
    if response.status_code == 200:
        print(response.json().get("message"))
    else:
        print(response.json().get("error", "Failed to delete item."))


def find_and_import_from_api():
    """Search OpenFoodFacts (via the API) and optionally import a product."""
    choice = input("Search by (1) barcode or (2) name? ").strip()

    if choice == "1":
        barcode = input("Enter barcode: ").strip()
        result = requests.get(f"{API_URL}/inventory/search/barcode/{barcode}")
        if result.status_code != 200:
            print("Product not found.")
            return
        product = result.json()
        print(f"Found: {product.get('product_name')} ({product.get('brands')})")
        confirm = input("Add to inventory? (y/n): ").strip().lower()
        if confirm == "y":
            quantity = input("Quantity: ").strip()
            price = input("Price: ").strip()
            payload = {
                "quantity": int(quantity) if quantity.isdigit() else 0,
                "price": float(price) if _is_number(price) else 0.0,
            }
            response = requests.post(
                f"{API_URL}/inventory/import/barcode/{barcode}", json=payload
            )
            if response.status_code == 201:
                print("Item imported successfully:")
                print_item(response.json())
            else:
                print("Failed to import item.")

    elif choice == "2":
        name = input("Enter product name: ").strip()
        result = requests.get(f"{API_URL}/inventory/search/name/{name}")
        if result.status_code != 200:
            print("No products found.")
            return
        products = result.json()
        for idx, p in enumerate(products, start=1):
            print(f"{idx}. {p.get('product_name')} ({p.get('brands')}) - barcode: {p.get('barcode')}")
        print("To import an item, note its barcode and choose option 1 (search by barcode).")

    else:
        print("Invalid choice.")


MENU_TEXT = """
==== Inventory Management CLI ====
1. View all items
2. View single item
3. Add new item
4. Update item
5. Delete item
6. Find & import item from external API
7. Exit
"""


def main_menu():
    """Main interactive loop for the CLI."""
    while True:
        print(MENU_TEXT)
        choice = input("Select an option: ").strip()
        if choice == "1":
            view_all_items()
        elif choice == "2":
            view_single_item()
        elif choice == "3":
            add_item()
        elif choice == "4":
            update_item()
        elif choice == "5":
            delete_item()
        elif choice == "6":
            find_and_import_from_api()
        elif choice == "7":
            print("Goodbye!")
            break
        else:
            print("Invalid option, try again.")


if __name__ == "__main__":
    main_menu()
