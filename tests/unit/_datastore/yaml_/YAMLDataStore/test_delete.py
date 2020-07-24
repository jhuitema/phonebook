"""Unit tests for the :meth:`YAMLDataStore.delete` method."""


import itertools
import yaml
import logging

import pytest

from phonebook._datastore.base import REQUIRED_FIELDS
from phonebook._datastore.yaml_ import YAMLDataStore
from phonebook._exceptions import MissingUserError, InvalidUserError


def test_main_case(data_store_path):
    """Test deleting a user."""
    data_set = [
        {"name": "Eric Idle", "phone": "123-456-7890", "address": "here"},
        {"name": "John Cleese", "phone": "111-222-3333", "address": "there"},
    ]
    data_store_path.write_text(yaml.dump(data_set))
    data_store = YAMLDataStore(file_path=str(data_store_path))
    assert data_store._users == data_set

    data_store.delete("Eric Idle")

    assert data_set[0] not in data_store._users
    assert data_set[0] not in yaml.safe_load(data_store_path.read_text())


def test_with_missing_user(data_store_path):
    """Test `delete` when the user doesn't exists."""
    data_set = [{"name": "Eric Idle", "phone": "123-456-7890", "address": "here"}]
    data_store_path.write_text(yaml.dump(data_set))
    data_store = YAMLDataStore(file_path=str(data_store_path))
    assert data_store._users == data_set

    with pytest.raises(MissingUserError) as error:
        data_store.delete("John Cleese")

    assert "John Cleese" in str(error.value)
