"""
test_cli.py

Unit tests for cli.py. The `requests` calls the CLI makes to the API
are mocked so these tests run without a live Flask server, and
`input()` is monkeypatched to simulate user interaction.
"""
from unittest.mock import patch, MagicMock

import cli


def _mock_response(json_data, status_code=200):
    mock_resp = MagicMock()
    mock_resp.status_code = status_code
    mock_resp.json.return_value = json_data
    return mock_resp


@patch("cli.requests.get")
def test_view_all_items_prints_items(mock_get, capsys):
    mock_get.return_value = _mock_response(
        [{"id": 1, "product_name": "Milk", "brand": "Silk", "quantity": 5, "price": 2.5}]
    )
    cli.view_all_items()
    captured = capsys.readouterr()
    assert "Milk" in captured.out


@patch("cli.requests.get")
def test_view_all_items_empty(mock_get, capsys):
    mock_get.return_value = _mock_response([])
    cli.view_all_items()
    captured = capsys.readouterr()
    assert "Inventory is empty." in captured.out


@patch("cli.requests.get")
def test_view_single_item_success(mock_get, capsys, monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "1")
    mock_get.return_value = _mock_response(
        {"id": 1, "product_name": "Milk", "brand": "Silk", "quantity": 5, "price": 2.5}
    )
    cli.view_single_item()
    captured = capsys.readouterr()
    assert "Milk" in captured.out


def test_view_single_item_invalid_id(capsys, monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "abc")
    cli.view_single_item()
    captured = capsys.readouterr()
    assert "Invalid ID." in captured.out


@patch("cli.requests.post")
def test_add_item_success(mock_post, capsys, monkeypatch):
    responses = iter(["Bread", "Dave's", "111", "10", "3.99"])
    monkeypatch.setattr("builtins.input", lambda _: next(responses))
    mock_post.return_value = _mock_response(
        {"id": 3, "product_name": "Bread", "brand": "Dave's", "quantity": 10, "price": 3.99},
        201,
    )
    cli.add_item()
    captured = capsys.readouterr()
    assert "Item added successfully" in captured.out
    assert "Bread" in captured.out


@patch("cli.requests.patch")
def test_update_item_success(mock_patch, capsys, monkeypatch):
    responses = iter(["1", "20", "1.99"])
    monkeypatch.setattr("builtins.input", lambda _: next(responses))
    mock_patch.return_value = _mock_response(
        {"id": 1, "product_name": "Milk", "quantity": 20, "price": 1.99}
    )
    cli.update_item()
    captured = capsys.readouterr()
    assert "Item updated successfully" in captured.out


def test_update_item_no_changes(capsys, monkeypatch):
    responses = iter(["1", "", ""])
    monkeypatch.setattr("builtins.input", lambda _: next(responses))
    cli.update_item()
    captured = capsys.readouterr()
    assert "No changes provided." in captured.out


@patch("cli.requests.delete")
def test_delete_item_success(mock_delete, capsys, monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "1")
    mock_delete.return_value = _mock_response({"message": "Item with id 1 deleted"})
    cli.delete_item()
    captured = capsys.readouterr()
    assert "deleted" in captured.out


@patch("cli.requests.post")
@patch("cli.requests.get")
def test_find_and_import_by_barcode(mock_get, mock_post, capsys, monkeypatch):
    responses = iter(["1", "999", "y", "5", "2.00"])
    monkeypatch.setattr("builtins.input", lambda _: next(responses))
    mock_get.return_value = _mock_response(
        {"product_name": "Peanut Butter", "brands": "Jif", "barcode": "999"}
    )
    mock_post.return_value = _mock_response(
        {"id": 3, "product_name": "Peanut Butter", "quantity": 5, "price": 2.00}, 201
    )
    cli.find_and_import_from_api()
    captured = capsys.readouterr()
    assert "Found: Peanut Butter" in captured.out
    assert "Item imported successfully" in captured.out


@patch("cli.requests.get")
def test_find_by_name(mock_get, capsys, monkeypatch):
    responses = iter(["2", "peanut"])
    monkeypatch.setattr("builtins.input", lambda _: next(responses))
    mock_get.return_value = _mock_response(
        [{"product_name": "Peanut Butter", "brands": "Jif", "barcode": "999"}]
    )
    cli.find_and_import_from_api()
    captured = capsys.readouterr()
    assert "Peanut Butter" in captured.out
