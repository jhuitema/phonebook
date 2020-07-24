"""Unit tests for the :meth:`JSONDataStore.update` method."""


import itertools
import json
import logging

import pytest

from phonebook._datastore.base import REQUIRED_FIELDS
from phonebook._datastore.json_ import JSONDataStore
from phonebook._exceptions import DuplicateUserError, MissingUserError, InvalidUserError


def test_with_same_name(data_store_path):
    """Test when updating a user with the same name."""
    data_set = [
        {"name": "Eric Idle", "phone": "123-456-7890", "address": "here"},
        {"name": "John Cleese", "phone": "111-222-3333", "address": "there"},
    ]
    data_store_path.write_text(json.dumps(data_set))
    data_store = JSONDataStore(file_path=str(data_store_path))
    assert data_store._users == data_set

    updated_user = {"name": "Eric Idle", "phone": "999-999-9999", "address": "not here"}
    data_store.update("Eric Idle", **updated_user)

    assert updated_user in data_store._users
    assert updated_user in json.loads(data_store_path.read_text())


def test_with_different_name(data_store_path):
    """Test when updating a user with a different name."""
    data_set = [
        {"name": "Eric Idle", "phone": "123-456-7890", "address": "here"},
        {"name": "John Cleese", "phone": "111-222-3333", "address": "there"},
    ]
    data_store_path.write_text(json.dumps(data_set))
    data_store = JSONDataStore(file_path=str(data_store_path))
    assert data_store._users == data_set

    updated_user = {
        "name": "Terry Gilliam",
        "phone": "999-999-9999",
        "address": "not here",
    }
    data_store.update("Eric Idle", **updated_user)

    assert updated_user in data_store._users
    assert not [user for user in data_store._users if user["name"] == "Eric Idle"]
    json_data = json.loads(data_store_path.read_text())
    assert updated_user in json_data
    assert not [user for user in json_data if user["name"] == "Eric Idle"]


def test_with_unknown_field(data_store_path, caplog):
    """Test `update` when the user has an unknown field."""
    caplog.set_level(logging.WARNING)
    data_set = [{"name": "Eric Idle", "phone": "123-456-7890", "address": "here"}]
    data_store_path.write_text(json.dumps(data_set))
    data_store = JSONDataStore(file_path=str(data_store_path))

    user = {"phone": "999-999-9999", "foobar": "baz"}
    data_store.update("Eric Idle", **user)

    expected_data = {"name": "Eric Idle", "phone": "999-999-9999", "address": "here"}
    assert expected_data in data_store._users
    assert expected_data in json.loads(data_store_path.read_text())

    for record in caplog.records:
        if "foobar" in record.getMessage():
            break
    else:
        pytest.fail("Unable to find warning message with unknown field 'foobar'")


def test_with_duplicate_user(data_store_path):
    """Test `update` when changing the name and the user already exists."""
    data_set = [
        {"name": "Eric Idle", "phone": "123-456-7890", "address": "here"},
        {"name": "John Cleese", "phone": "111-222-3333", "address": "there"},
    ]
    data_store_path.write_text(json.dumps(data_set))
    data_store = JSONDataStore(file_path=str(data_store_path))
    assert data_store._users == data_set

    updated_user = {
        "name": "John Cleese",
        "phone": "999-999-9999",
        "address": "not here",
    }
    with pytest.raises(DuplicateUserError) as error:
        data_store.update("Eric Idle", **updated_user)

    assert "John Cleese" in str(error.value)


def test_with_missing_user(data_store_path):
    """Test `update` when the user doesn't exists."""
    data_set = [{"name": "Eric Idle", "phone": "123-456-7890", "address": "here"}]
    data_store_path.write_text(json.dumps(data_set))
    data_store = JSONDataStore(file_path=str(data_store_path))
    assert data_store._users == data_set

    user = {"name": "John Cleese", "phone": "999-999-9999", "address": "not here"}
    with pytest.raises(MissingUserError) as error:
        data_store.update("John Cleese", **user)

    assert "John Cleese" in str(error.value)
