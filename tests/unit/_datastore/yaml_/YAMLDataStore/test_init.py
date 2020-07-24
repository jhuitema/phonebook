"""Unit tests for the :meth:`YAMLDataStore.__init__` method."""


import yaml

from phonebook._datastore.yaml_ import YAMLDataStore


def test_without_file(data_store_path):
    """Test creating a data store when the YAML file doesn't exist."""
    assert not data_store_path.exists()
    data_store = YAMLDataStore(file_path=str(data_store_path))
    assert data_store
    assert data_store._users == []


def test_with_empty_file(data_store_path):
    """Test creating a data store when the YAML file is empty."""
    data_set = []
    data_store_path.write_text(yaml.dump(data_set))

    assert data_store_path.exists()
    data_store = YAMLDataStore(file_path=str(data_store_path))
    assert data_store
    assert data_store._users == []


def test_with_single_user(data_store_path):
    """Test creating a data store when the YAML file contains one user."""
    data_set = [
        {"name": "Eric Idle", "phone": "123-456-7890", "address": "here"},
    ]
    data_store_path.write_text(yaml.dump(data_set))

    assert data_store_path.exists()
    data_store = YAMLDataStore(file_path=str(data_store_path))
    assert data_store
    assert data_store._users == data_set


def test_with_multiple_users(data_store_path):
    """Test creating a data store when the YAML file has many users."""
    data_set = [
        {"name": "Eric Idle", "phone": "123-456-7890", "address": "here"},
        {"name": "John Cleese", "phone": "111-222-3333", "address": "there"},
        {"name": "Terry Gilliam", "phone": "555-555-5555", "address": "not here"},
    ]
    data_store_path.write_text(yaml.dump(data_set))

    assert data_store_path.exists()
    data_store = YAMLDataStore(file_path=str(data_store_path))
    assert data_store
    assert data_store._users == data_set
