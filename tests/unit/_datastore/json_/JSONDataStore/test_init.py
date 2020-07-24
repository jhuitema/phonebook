"""Unit tests for the :meth:`JSONDataStore.__init__` method."""


import json

from phonebook._datastore.json_ import JSONDataStore


def test_without_file(data_store_path):
    """Test creating a data store when the JSON file doesn't exist."""
    assert not data_store_path.exists()
    data_store = JSONDataStore(file_path=str(data_store_path))
    assert data_store
    assert data_store._users == []


def test_with_empty_file(data_store_path):
    """Test creating a data store when the JSON file is empty."""
    data_set = []
    data_store_path.write_text(json.dumps(data_set))

    assert data_store_path.exists()
    data_store = JSONDataStore(file_path=str(data_store_path))
    assert data_store
    assert data_store._users == []


def test_name(data_store_path):
    """Test the data store has a name defined."""
    assert not data_store_path.exists()
    data_store = JSONDataStore(file_path=str(data_store_path))
    assert data_store.NAME == "json"


def test_with_single_user(data_store_path):
    """Test creating a data store when the JSON file contains one user."""
    data_set = [
        {"name": "Eric Idle", "phone": "123-456-7890", "address": "here"},
    ]
    data_store_path.write_text(json.dumps(data_set))

    assert data_store_path.exists()
    data_store = JSONDataStore(file_path=str(data_store_path))
    assert data_store
    assert data_store._users == data_set


def test_with_multiple_users(data_store_path):
    """Test creating a data store when the JSON file has many users."""
    data_set = [
        {"name": "Eric Idle", "phone": "123-456-7890", "address": "here"},
        {"name": "John Cleese", "phone": "111-222-3333", "address": "there"},
        {"name": "Terry Gilliam", "phone": "555-555-5555", "address": "not here"},
    ]
    data_store_path.write_text(json.dumps(data_set))

    assert data_store_path.exists()
    data_store = JSONDataStore(file_path=str(data_store_path))
    assert data_store
    assert data_store._users == data_set
