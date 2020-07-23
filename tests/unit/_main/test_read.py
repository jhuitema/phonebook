"""Unit tests for the :meth:`phonebook.read` method."""


import pytest

import phonebook


_FILTERS = {"name": "*", "phone": "*", "address": "*"}


@pytest.mark.parametrize("filters", (None, _FILTERS))
def test_with_data_store(mocker, filters):
    """Test when the data store is already set."""
    mock_data_store = mocker.MagicMock(spec=phonebook._datastore.base.BaseDataStore)
    mocker.patch.object(phonebook._main, "_DATA_STORE", mock_data_store)

    phonebook.read(filters=filters)

    mock_data_store.read.assert_called_once_with(filters=filters)


@pytest.mark.parametrize("filters", (None, _FILTERS))
def test_without_data_store(mocker, filters):
    """Test when the data store is not already set."""
    mock_data_store = mocker.MagicMock(spec=phonebook._datastore.base.BaseDataStore)
    mock_default_data_store = mocker.MagicMock(return_value=mock_data_store)
    mocker.patch.object(phonebook._main, "_DATA_STORE", None)
    mocker.patch.object(phonebook._main, "_DEFAULT_DATA_STORE", mock_default_data_store)

    phonebook.read(filters=filters)

    mock_data_store.read.assert_called_once_with(filters=filters)
