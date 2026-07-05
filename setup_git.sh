#!/usr/bin/env bash
set -e

git init -b main

# --- Initial commit (required so 'main' exists before branching) -----------
git add .gitignore
git commit -m "chore: initial commit"

# --- Feature 1: data store -------------------------------------------------
git checkout -b feature/data-store
git add data_store.py
git commit -m "feat: add in-memory inventory data store"
git checkout main
git merge --no-ff feature/data-store -m "Merge branch 'feature/data-store'"
git branch -d feature/data-store

# --- Feature 2: external API integration -----------------------------------
git checkout -b feature/external-api
git add external_api.py
git commit -m "feat: integrate OpenFoodFacts external API"
git checkout main
git merge --no-ff feature/external-api -m "Merge branch 'feature/external-api'"
git branch -d feature/external-api

# --- Feature 3: Flask REST API (CRUD + helper routes) -----------------------
git checkout -b feature/flask-api
git add app.py
git commit -m "feat: add Flask REST API with full CRUD and helper routes"
git checkout main
git merge --no-ff feature/flask-api -m "Merge branch 'feature/flask-api'"
git branch -d feature/flask-api

# --- Feature 4: CLI frontend -------------------------------------------------
git checkout -b feature/cli
git add cli.py
git commit -m "feat: add CLI frontend for interacting with the API"
git checkout main
git merge --no-ff feature/cli -m "Merge branch 'feature/cli'"
git branch -d feature/cli

# --- Feature 5: tests --------------------------------------------------------
git checkout -b feature/tests
git add tests/ pytest.ini
git commit -m "test: add pytest suite covering routes, CLI, and external API"
git checkout main
git merge --no-ff feature/tests -m "Merge branch 'feature/tests'"
git branch -d feature/tests

# --- Feature 6: docs & project config ----------------------------------------
git checkout -b feature/docs
git add README.md requirements.txt setup_git.sh
git commit -m "docs: add README, requirements, and setup script"
git checkout main
git merge --no-ff feature/docs -m "Merge branch 'feature/docs'"
git branch -d feature/docs

echo ""
echo "=========================================================="
echo "Local git history created with feature branches merged into main."
echo "=========================================================="
