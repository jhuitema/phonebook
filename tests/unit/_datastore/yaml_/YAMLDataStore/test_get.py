"""Unit tests for the :meth:`YAMLDataStore.get` method."""


import yaml

import pytest

from phonebook._datastore.yaml_ import YAMLDataStore
from phonebook._exceptions import MissingUserError


def test_main_case(data_store_path):
    """Test getting a user by name."""
    data_set = [
        {"name": "Eric Idle", "phone": "123-456-7890", "address": "here"},
        {"name": "John Cleese", "phone": "111-222-3333", "address": "there"},
    ]
    data_store_path.write_text(yaml.dump(data_set))
    data_store = YAMLDataStore(file_path=str(data_store_path))
    assert data_store._users == data_set

    result = data_store.get("Eric Idle")

    expected_result = {"name": "Eric Idle", "phone": "123-456-7890", "address": "here"}
    assert result == expected_result


def test_with_missing_user(data_store_path):
    """Test `get` when the user doesn't exists."""
    data_set = [{"name": "Eric Idle", "phone": "123-456-7890", "address": "here"}]
    data_store_path.write_text(yaml.dump(data_set))
    data_store = YAMLDataStore(file_path=str(data_store_path))
    assert data_store._users == data_set

    with pytest.raises(MissingUserError) as error:
        data_store.get("John Cleese")

    assert "John Cleese" in str(error.value)
