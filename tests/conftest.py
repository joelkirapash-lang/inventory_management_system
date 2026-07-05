"""
conftest.py

Shared pytest fixtures. Ensures every test starts from a known,
predictable inventory state regardless of test execution order.
"""
import os
import sys

# Make the project root importable when running `pytest` from the repo root.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest

import data_store
import app as app_module


@pytest.fixture(autouse=True)
def reset_inventory():
    """Reset the in-memory inventory before every single test."""
    data_store.reset()
    yield
    data_store.reset()


@pytest.fixture
def client():
    """Flask test client for hitting API routes directly."""
    app_module.app.config["TESTING"] = True
    with app_module.app.test_client() as test_client:
        yield test_client
