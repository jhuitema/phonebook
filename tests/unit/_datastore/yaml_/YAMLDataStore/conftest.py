"""Fixtures for the `phonebook._datastore.yaml_` unit tests."""


import pytest


@pytest.fixture()
def data_store_path(tmp_path):
    """Get the path to use as the source of the data store.

    Returns:
        pathlib.Path: The path to use as the data store.

    """
    return tmp_path / "test_data_source.yaml"
