"""
data_store.py

Simulated in-memory data storage for the Inventory Management System.
In a production system this would be replaced by a real database
(e.g. SQLite/PostgreSQL). For this lab, a Python list of dictionaries
acts as our "database array".

Each item is structured to resemble data returned by the OpenFoodFacts
API, with an added `id`, `quantity`, and `price` for inventory purposes.
"""

inventory = [
    {
        "id": 1,
        "product_name": "Organic Almond Milk",
        "brand": "Silk",
        "barcode": "0025293001165",
        "quantity": 50,
        "price": 3.99,
        "ingredients_text": "Filtered water, almonds, cane sugar",
    },
    {
        "id": 2,
        "product_name": "Whole Wheat Bread",
        "brand": "Dave's Killer Bread",
        "barcode": "0787359110107",
        "quantity": 30,
        "price": 5.49,
        "ingredients_text": "Whole wheat flour, water, honey, yeast",
    },
]

_next_id = 3


def get_next_id():
    """Return the next available unique ID and increment the counter."""
    global _next_id
    current = _next_id
    _next_id += 1
    return current


def reset(seed_data=None, next_id=3):
    """
    Reset the inventory to a known state. Primarily used by the test
    suite to make tests independent of one another.
    """
    global _next_id
    inventory.clear()
    if seed_data is None:
        seed_data = [
            {
                "id": 1,
                "product_name": "Organic Almond Milk",
                "brand": "Silk",
                "barcode": "0025293001165",
                "quantity": 50,
                "price": 3.99,
                "ingredients_text": "Filtered water, almonds, cane sugar",
            },
            {
                "id": 2,
                "product_name": "Whole Wheat Bread",
                "brand": "Dave's Killer Bread",
                "barcode": "0787359110107",
                "quantity": 30,
                "price": 5.49,
                "ingredients_text": "Whole wheat flour, water, honey, yeast",
            },
        ]
    inventory.extend(seed_data)
    _next_id = next_id
