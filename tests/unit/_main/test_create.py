"""Unit tests for the :meth:`phonebook.create` method."""


import phonebook


_USER = {"name": "Eric Idle", "phone": "123-456-7890", "address": "here"}


def test_with_data_store(mocker):
    """Test when the data store is already set."""
    mock_data_store = mocker.MagicMock(spec=phonebook._datastore.base.BaseDataStore)
    mocker.patch.object(phonebook._main, "_DATA_STORE", mock_data_store)

    phonebook.create(_USER)

    mock_data_store.create.assert_called_once_with(_USER)


def test_without_data_store(mocker):
    """Test when the data store is not already set."""
    mock_data_store = mocker.MagicMock(spec=phonebook._datastore.base.BaseDataStore)
    mock_default_data_store = mocker.MagicMock(return_value=mock_data_store)
    mocker.patch.object(phonebook._main, "_DATA_STORE", None)
    mocker.patch.object(phonebook._main, "_DEFAULT_DATA_STORE", mock_default_data_store)

    phonebook.create(_USER)

    mock_data_store.create.assert_called_once_with(_USER)
