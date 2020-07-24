"""The JSON data store used to access the information for Phonebook."""


import copy
import fnmatch
import logging
import os

import json

from .. import _exceptions
from . import base


_LOGGER = logging.getLogger(__name__)


class JSONDataStore(base.BaseDataStore):
    """The JSON data store used to access the information for Phonebook."""

    _DEFAULT_PATH = os.path.expandvars("$HOME/phonebook.json")
    NAME = "json"

    def __init__(self, file_path=None):
        """Initialize the data store.

        Keyword Args:
            file_path (str): The path of the JSON file the data store
                will read. If None, then the default path will be used.

        """
        self._file_path = file_path or self._DEFAULT_PATH
        if os.path.exists(self._file_path):
            self.reload()
        else:
            self._users = []
            self._write()

    def read(self, filters=None):
        """Get user information from the data store.

        Keyword Args:
            filters (dict(str, str) or None): The filters to use to
                restrict the user information returned. Each key of the
                dictionary is the name of the field to filter by. Each
                value is a :mod:`fnmatch`-compliant string that must be
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
        filters = filters or {}
        result = []
        for user in self._users:
            user_matches = True
            for field, pattern in filters.items():
                if not fnmatch.fnmatch(user[field], pattern):
                    user_matches = False
                    break
            if user_matches:
                result.append(user)

        return result

    def create(self, user):
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
        user = base.validate(user)

        # ensure the given user doesn't already exist
        for existing_user in self._users:
            if user["name"] == existing_user["name"]:
                raise _exceptions.DuplicateUserError(
                    f"User '{user['name']}' already exists in the data store!"
                )

        self._users.append(user)
        self._write()

    def delete(self, name):
        """Delete the user with given `name` from the data store.

        Args:
            name (str): The name of the user to delete from the data
                store.

        Raises:
            MissingUserError: Raised when a user with the given `name`
                does not exist in the data store.

        """
        user_index = None
        # ensure the given user exists
        for index, existing_user in enumerate(self._users):
            if name == existing_user["name"]:
                user_index = index
                break
        else:
            raise _exceptions.MissingUserError(
                f"User '{name}' does not exist in the data store!"
            )

        self._users.pop(user_index)
        self._write()

    def update(self, user_name, **user_fields):
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
        user_fields = base.validate(user_fields, ignore_required_fields=True)
        user_index = None
        original_user = None
        using_same_name = user_name == user_fields.get("name", user_name)

        for index, existing_user in enumerate(self._users):
            # ensure the given user exists
            if user_name == existing_user["name"]:
                user_index = index
                original_user = existing_user
                # only `break` if the user name hasn't changed,
                # otherwise the rest of the users still need to be
                # checked
                if using_same_name:
                    break
            # ensure the given user doesn't already exist (if they
            # changed the user name)
            elif not using_same_name and user_fields["name"] == existing_user["name"]:
                raise _exceptions.DuplicateUserError(
                    f"User '{user_fields['name']}' already exists in the data store!"
                )

        if user_index is None or original_user is None:
            raise _exceptions.MissingUserError(
                f"User '{user_name}' does not exist in the data store!"
            )

        updated_user = copy.copy(original_user)
        updated_user.update(user_fields)
        self._users[user_index] = updated_user
        self._write()

    def reload(self):
        """Reload the internal data store from the JSON file."""
        _LOGGER.debug(f"Reloading data store: {self._file_path}")
        with open(self._file_path) as data_file:
            self._users = json.load(data_file)

    def _write(self):
        """Write the internal data store to the JSON file."""
        _LOGGER.debug(f"Writing to data store: {self._file_path}")
        with open(self._file_path, "w") as data_file:
            json.dump(self._users, data_file, indent=2)
