"""Unit tests for the :meth:`JSONDataStore.read` method."""


import itertools
import json
import logging

import pytest

from phonebook._datastore.base import REQUIRED_FIELDS
from phonebook._datastore.json_ import JSONDataStore
from phonebook._exceptions import DuplicateUserError, InvalidUserError


def test_with_empty_data_store(data_store_path):
    """Test creating a user when the data store is empty."""
    data_set = []
    data_store_path.write_text(json.dumps(data_set))
    data_store = JSONDataStore(file_path=str(data_store_path))
    assert data_store._users == data_set

    data_store.create({"name": "Eric Idle", "phone": "123-456-7890", "address": "here"})

    expected_data = [{"name": "Eric Idle", "phone": "123-456-7890", "address": "here"}]
    assert data_store._users == expected_data
    assert json.loads(data_store_path.read_text()) == expected_data


def test_with_populated_file(data_store_path):
    """Test creating a user when the data store is not empty."""
    data_set = [
        {"name": "John Cleese", "phone": "111-222-3333", "address": "there"},
    ]
    data_store_path.write_text(json.dumps(data_set))
    data_store = JSONDataStore(file_path=str(data_store_path))
    assert data_store._users == data_set

    data_store.create({"name": "Eric Idle", "phone": "123-456-7890", "address": "here"})

    expected_data = [
        {"name": "John Cleese", "phone": "111-222-3333", "address": "there"},
        {"name": "Eric Idle", "phone": "123-456-7890", "address": "here"},
    ]
    assert data_store._users == expected_data
    assert json.loads(data_store_path.read_text()) == expected_data


@pytest.mark.parametrize(
    "missing_fields",
    # get all combinations of any length (other than 0)
    itertools.chain.from_iterable(
        itertools.combinations(REQUIRED_FIELDS, length)
        for length in range(1, len(REQUIRED_FIELDS))
    ),
)
def test_with_missing_required_fields(data_store_path, missing_fields):
    """Test `create` when the user is missing a required field."""
    data_store = JSONDataStore(file_path=str(data_store_path))
    user = {"name": "Eric Idle", "phone": "123-456-7890", "address": "here"}
    for missing_field in missing_fields:
        del user[missing_field]

    with pytest.raises(InvalidUserError) as error:
        data_store.create(user)

    error_msg = str(error.value)
    for missing_field in missing_fields:
        assert missing_field in error_msg


def test_with_unknown_field(data_store_path, caplog):
    """Test `create` when the user has an unknown field."""
    caplog.set_level(logging.WARNING)
    data_store = JSONDataStore(file_path=str(data_store_path))

    user = {
        "name": "Eric Idle",
        "phone": "123-456-7890",
        "address": "here",
        "foobar": "baz",
    }
    data_store.create(user)

    expected_data = [{"name": "Eric Idle", "phone": "123-456-7890", "address": "here"}]
    assert data_store._users == expected_data
    assert json.loads(data_store_path.read_text()) == expected_data

    for record in caplog.records:
        if "foobar" in record.getMessage():
            break
    else:
        pytest.fail("Unable to find warning message with unknown field 'foobar'")


def test_with_duplicate_user(data_store_path):
    """Test `create` when the user already exists."""
    data_set = [{"name": "Eric Idle", "phone": "123-456-7890", "address": "here"}]
    data_store_path.write_text(json.dumps(data_set))
    data_store = JSONDataStore(file_path=str(data_store_path))
    assert data_store._users == data_set

    user = {"name": "Eric Idle", "phone": "999-999-9999", "address": "not here"}
    with pytest.raises(DuplicateUserError) as error:
        data_store.create(user)

    assert "Eric Idle" in str(error.value)
