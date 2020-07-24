"""Unit tests for the :meth:`JSONDataStore.__init__` method."""


import json

from phonebook._datastore.json_ import JSONDataStore


def test_updates_to_file(data_store_path):
    """Test reloading a data store when the JSON file has changed."""
    data_store_path.write_text(json.dumps([]))
    data_store = JSONDataStore(file_path=str(data_store_path))
    # change the file after the class has loaded the empty file into
    # memory
    data_set = [{"name": "Eric Idle", "phone": "123-456-7890", "address": "here"}]
    data_store_path.write_text(json.dumps(data_set))

    data_store.reload()

    assert data_store._users == data_set


def test_updates_to_data_store(data_store_path):
    """Test reloading a data store wipes any unsaved changes."""
    data_store_path.write_text(json.dumps([]))
    data_store = JSONDataStore(file_path=str(data_store_path))
    data_store._users = [
        {"name": "Eric Idle", "phone": "123-456-7890", "address": "here"}
    ]

    data_store.reload()

    assert data_store._users == []
