"""Unit tests for the :meth:`phonebook.set_data_store` method."""


import pytest

import phonebook


def test_with_data_store(mocker):
    """Test when the data store is already set."""
    mock_data_store = mocker.MagicMock(spec=phonebook._datastore.base.BaseDataStore)
    mocker.patch.object(phonebook._main, "_DATA_STORE", mock_data_store)

    new_data_store = mocker.MagicMock(spec=phonebook._datastore.base.BaseDataStore)
    phonebook.set_data_store(new_data_store)

    assert phonebook._main._DATA_STORE == new_data_store


def test_without_data_store(mocker):
    """Test when the data store is not already set."""
    mocker.patch.object(phonebook._main, "_DATA_STORE", None)

    new_data_store = mocker.MagicMock(spec=phonebook._datastore.base.BaseDataStore)
    phonebook.set_data_store(new_data_store)

    assert phonebook._main._DATA_STORE == new_data_store


def test_invalid_data_store():
    """Test when the data store is not a BaseDataStore subclass."""
    with pytest.raises(TypeError) as error:
        phonebook.set_data_store("not a valid data store")
        assert "str" in str(error.value)
