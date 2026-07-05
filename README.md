# Inventory Management System

A Flask REST API + CLI for managing e-commerce inventory, built for the
Moringa School Summative Lab. Includes full CRUD, integration with the
[OpenFoodFacts API](https://world.openfoodfacts.org/), a command-line
interface, and a pytest test suite.

## Features

- **Flask REST API** with full CRUD (`GET`, `POST`, `PATCH`, `DELETE`) plus
  helper routes (`/health`, external-search, external-import).
- **OpenFoodFacts integration** to look up real product data by barcode or
  name and optionally add it straight to inventory.
- **CLI tool** that talks to the API so you can add, view, update, delete,
  and import items from the terminal.
- **Test suite** (pytest + `unittest.mock`) covering every route, the
  external API wrapper, and every CLI command.

## Project Structure

```
inventory_management_system/
├── app.py              # Flask REST API (routes)
├── data_store.py        # In-memory "database array"
├── external_api.py      # OpenFoodFacts integration
├── cli.py               # CLI frontend
├── requirements.txt
├── pytest.ini
├── setup_git.sh          # Optional: sets up a feature-branch git history
├── .gitignore
├── README.md
└── tests/
    ├── conftest.py
    ├── test_crud_routes.py
    ├── test_external_api.py
    ├── test_external_api_routes.py
    └── test_cli.py
```

## Installation & Setup

1. **Clone the repo** and move into it:
   ```bash
   git clone https://github.com/<your-username>/<your-repo>.git
   cd inventory_management_system
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate   # on Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Running the API

```bash
python app.py
```

The server starts at `http://127.0.0.1:5000` in debug mode.

## Running the CLI

In a **second terminal** (with the API still running):

```bash
python cli.py
```

You'll see a menu:

```
==== Inventory Management CLI ====
1. View all items
2. View single item
3. Add new item
4. Update item
5. Delete item
6. Find & import item from external API
7. Exit
```

### Example session

```
Select an option: 6
Search by (1) barcode or (2) name? 1
Enter barcode: 3017620422003
Found: Nutella (Ferrero)
Add to inventory? (y/n): y
Quantity: 25
Price: 4.99
Item imported successfully:
----------------------------------------
ID: 3
Product: Nutella
Brand: Ferrero
...
```

## API Endpoints

| Method | Endpoint                              | Description                                      |
|--------|----------------------------------------|--------------------------------------------------|
| GET    | `/`                                     | Welcome message                                   |
| GET    | `/health`                                | Health check + item count                        |
| GET    | `/inventory`                             | Fetch all items                                   |
| GET    | `/inventory/<id>`                        | Fetch a single item                               |
| POST   | `/inventory`                             | Add a new item (JSON body)                        |
| PATCH  | `/inventory/<id>`                        | Update an existing item (JSON body)               |
| DELETE | `/inventory/<id>`                        | Delete an item                                    |
| GET    | `/inventory/search/barcode/<barcode>`    | Look up a product on OpenFoodFacts by barcode     |
| GET    | `/inventory/search/name/<name>`          | Search OpenFoodFacts by product name              |
| POST   | `/inventory/import/barcode/<barcode>`    | Fetch by barcode and add straight to inventory    |

### Example: create an item

```bash
curl -X POST http://127.0.0.1:5000/inventory \
  -H "Content-Type: application/json" \
  -d '{"product_name": "Sparkling Water", "brand": "LaCroix", "quantity": 20, "price": 4.25}'
```

### Example: update an item

```bash
curl -X PATCH http://127.0.0.1:5000/inventory/1 \
  -H "Content-Type: application/json" \
  -d '{"quantity": 5}'
```

## Running Tests

```bash
pytest
```

For verbose output:

```bash
pytest -v
```

The suite mocks all external HTTP calls (`unittest.mock`), so it runs fully
offline and deterministically. It covers:

- Every CRUD route (success + error cases)
- The external API wrapper functions (found / not found / network failure)
- The external-API Flask routes (search + import)
- Every CLI command, with `input()` and `requests` mocked

## Git Workflow

This project follows a feature-branch workflow. If you'd like to reproduce
that commit history locally (useful for the "Git Management" rubric item),
run:

```bash
bash setup_git.sh
```

This creates a branch per feature (`feature/data-store`, `feature/flask-api`,
`feature/cli`, `feature/tests`, etc.), commits the relevant files on each
branch, merges each one back into `main` with `--no-ff`, and deletes the
branch afterward — then prints the commands to push to GitHub.

If you'd rather do it manually:

```bash
git checkout -b feature/my-feature
# ... make changes, git add, git commit ...
git checkout main
git merge --no-ff feature/my-feature
git branch -d feature/my-feature
git push origin main
```

## Notes

- Data is stored in-memory (a Python list) and resets whenever the Flask
  server restarts — this matches the lab's "simulated data storage" spec.
- Debugging: run with `FLASK_DEBUG=1 python app.py` for auto-reload and
  detailed error pages, or test endpoints with Postman/curl.
