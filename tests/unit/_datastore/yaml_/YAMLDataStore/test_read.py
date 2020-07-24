"""Unit tests for the :meth:`YAMLDataStore.read` method."""


import itertools
import yaml

import pytest

from phonebook._datastore.base import REQUIRED_FIELDS
from phonebook._datastore.yaml_ import YAMLDataStore


def test_with_empty_file_no_filters(data_store_path):
    """Test reading an empty data store with no filters."""
    data_set = []
    data_store_path.write_text(yaml.dump(data_set))
    data_store = YAMLDataStore(file_path=str(data_store_path))

    result = data_store.read()
    assert result == data_set


def test_with_single_user_no_filters(data_store_path):
    """Test reading a single-user data store with no filters."""
    data_set = [
        {"name": "Eric Idle", "phone": "123-456-7890", "address": "there"},
    ]
    data_store_path.write_text(yaml.dump(data_set))
    data_store = YAMLDataStore(file_path=str(data_store_path))

    result = data_store.read()
    assert result == data_set


def test_with_multiple_users_no_filters(data_store_path):
    """Test reading a multiple-user data store with no filters."""
    data_set = [
        {"name": "Eric Idle", "phone": "123-456-7890", "address": "there"},
        {"name": "John Cleese", "phone": "111-222-3333", "address": "here"},
        {"name": "Terry Gilliam", "phone": "555-555-5555", "address": "not found"},
    ]
    data_store_path.write_text(yaml.dump(data_set))
    data_store = YAMLDataStore(file_path=str(data_store_path))

    result = data_store.read()
    assert result == data_set


@pytest.mark.parametrize(
    "filters",
    (
        {"name": "Michael Palin"},
        {"phone": "999-999-9999"},
        {"address": "Camelot"},
        {"name": "Michael *", "phone": "*9*"},
    ),
)
def test_without_match(data_store_path, filters):
    """Test reading when no filters match."""
    data_set = [
        {"name": "Eric Idle", "phone": "123-456-7890", "address": "there"},
        {"name": "John Cleese", "phone": "111-222-3333", "address": "here"},
        {"name": "Terry Gilliam", "phone": "555-555-5555", "address": "not found"},
    ]
    data_store_path.write_text(yaml.dump(data_set))
    data_store = YAMLDataStore(file_path=str(data_store_path))

    result = data_store.read(filters=filters)
    assert result == []


@pytest.mark.parametrize(
    "exact_filters",
    # all combinations of any length (other than 0)
    itertools.chain.from_iterable(
        itertools.combinations(
            [("name", "Eric Idle"), ("phone", "123-456-7890"), ("address", "there")],
            length,
        )
        for length in range(1, len(REQUIRED_FIELDS))
    ),
)
def test_matching_exact_filter(data_store_path, exact_filters):
    """Test reading with an exact filter."""
    data_set = [
        {"name": "Eric Idle", "phone": "123-456-7890", "address": "there"},
        {"name": "John Cleese", "phone": "111-222-3333", "address": "here"},
        {"name": "Terry Gilliam", "phone": "555-555-5555", "address": "not found"},
    ]
    data_store_path.write_text(yaml.dump(data_set))
    data_store = YAMLDataStore(file_path=str(data_store_path))

    result = data_store.read(filters=dict(exact_filters))
    assert result == [data_set[0]]


@pytest.mark.parametrize(
    "fuzzy_filters",
    # all combinations of any length (other than 0)
    itertools.chain.from_iterable(
        itertools.combinations(
            [("name", "Eric *"), ("phone", "123-*-7890"), ("address", "?here")], length
        )
        for length in range(1, len(REQUIRED_FIELDS))
    ),
)
def test_fuzzy_filter_single_result(data_store_path, fuzzy_filters):
    """Test reading with a fuzzy filter with one result."""
    data_set = [
        {"name": "Eric Idle", "phone": "123-456-7890", "address": "there"},
        {"name": "John Cleese", "phone": "111-222-3333", "address": "here"},
        {"name": "Terry Gilliam", "phone": "555-555-5555", "address": "not found"},
    ]
    data_store_path.write_text(yaml.dump(data_set))
    data_store = YAMLDataStore(file_path=str(data_store_path))

    result = data_store.read(filters=dict(fuzzy_filters))
    assert result == [data_set[0]]


@pytest.mark.parametrize(
    "fuzzy_filters",
    # all combinations of any length (other than 0)
    itertools.chain.from_iterable(
        itertools.combinations(
            [("name", "* *e"), ("phone", "1*"), ("address", "*here")], length
        )
        for length in range(1, len(REQUIRED_FIELDS))
    ),
)
def test_fuzzy_filter_multiple_result(data_store_path, fuzzy_filters):
    """Test reading with a fuzzy filter with multiple results."""
    data_set = [
        {"name": "Eric Idle", "phone": "123-456-7890", "address": "there"},
        {"name": "John Cleese", "phone": "111-222-3333", "address": "here"},
        {"name": "Terry Gilliam", "phone": "555-555-5555", "address": "not found"},
    ]
    data_store_path.write_text(yaml.dump(data_set))
    data_store = YAMLDataStore(file_path=str(data_store_path))

    result = data_store.read(filters=dict(fuzzy_filters))
    assert result == [data_set[0], data_set[1]]
