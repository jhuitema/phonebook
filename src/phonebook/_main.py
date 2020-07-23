"""Main functionality for the Phonebook library."""


import logging

from . import _datastore
from ._datastore import json_ as json_datastore


_DATA_STORE = None
_DEFAULT_DATA_STORE = json_datastore.JSONDataStore
_LOGGER = logging.getLogger(__name__)


def set_data_store(data_store):
    """Set the data store to use.

    Args:
        data_store (BaseDataStore): A :class:`BaseDataStore` subclass to
            use for the public interface.

    Raises:
        TypeError: Raised when the given `data_store` is not a subclass
            of `BaseDataStore`.

    """
    if not isinstance(data_store, _datastore.base.BaseDataStore):
        # raise RuntimeError(data_store.__class__.__name__)
        raise TypeError(
            f"'{data_store.__class__.__name__}' is not a valid subclass of BaseDataStore"
        )
    global _DATA_STORE
    _LOGGER.debug(f"Setting data store to {data_store.__class__.__name__}")
    _DATA_STORE = data_store


def get(name):
    """Get a single user's information from the data store.

    Args:
        name (str): The name of the user to get from the data store.

    Returns:
        dict(str, str): The information for the requested user.

    Raises:
        MissingUserError: Raised when the requested user does not
            exist in the data store.

    """
    if not _DATA_STORE:
        set_data_store(_DEFAULT_DATA_STORE())
    _LOGGER.debug(f"Getting user: {name}")
    return _DATA_STORE.get(name)


def read(filters=None):
    """Get user information from the data store.

    Keyword Args:
        filters (dict(str, str) or None): The filters to use to
            restrict the user information returned. Each key of the
            dictionary is the name of the field to filter by. Each
            value is a :mod:`glob`-compliant string that must be
            true for the named field in order for the user to be
            returned.

            If multiple filters are provided, ALL filters must be
            valid for a user's information for it to be returned.

            If None then no filters are applied and all user
            information is returned.

    Returns:
        list(dict): The list of information for each user that
        matches the given `filters`.

    """
    if not _DATA_STORE:
        set_data_store(_DEFAULT_DATA_STORE())
    _LOGGER.debug(f"Reading users with filters: {str(filters)}")
    return _DATA_STORE.read(filters=filters)


def create(user):
    """Add the given `user` to the data store.

    Args:
        user (dict(str, str)): The user information to add to the
            data store.

    Raises:
        InvalidUserError: Raised when the given user does not
            provide needed information for a user.
        DuplicateUserError: Raised when a user with the given `name`
            already exists in the data store.

    """
    if not _DATA_STORE:
        set_data_store(_DEFAULT_DATA_STORE())
    _LOGGER.debug(f"Creating user: {user}")
    _DATA_STORE.create(user)


def delete(name):
    """Delete the user with given `name` from the data store.

    Args:
        name (str): The name of the user to delete from the data
            store.

    Raises:
        MissingUserError: Raised when a user with the given `name`
            does not exist in the data store.

    """
    if not _DATA_STORE:
        set_data_store(_DEFAULT_DATA_STORE())
    _LOGGER.debug(f"Deleting user: {name}")
    _DATA_STORE.delete(name)


def update(user_name, **user_fields):
    """Update the user with the given `user_name` in the data store.

    Args:
        user_name (str): The name of the user to update from the
            data store.

    Keyword Args:
        **user_fields (dict): The user information to replace the
            requested user's information with. The valid options
            are:

            * **name**: The name to update the user to.
            * **phone**: The phone number to update the user to.
            * **address**: The address to update the user to.

    Raises:
        MissingUserError: Raised when a user with the given `name`
            does not exist in the data store.
        DuplicateUserError: Raised when a `name` field was given
            that already exists in the Phonebook.

    """
    if not _DATA_STORE:
        set_data_store(_DEFAULT_DATA_STORE())
    _LOGGER.debug(f"Updating '{user_name}' user to: {str(user_fields)}")
    _DATA_STORE.update(user_name, **user_fields)
