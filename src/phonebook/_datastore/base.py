"""The base data store used to access the information for Phonebook."""


import abc
import logging

from .. import _exceptions


_LOGGER = logging.getLogger(__name__)
REQUIRED_FIELDS = {"name", "phone", "address"}


def validate(user, ignore_required_fields=False):
    """Validate the given `user` is a valid user dictionary.

    Args:
        user (dict(str, str)): The user information to validate.

    Keyword Args:
        ignore_required_fields (bool): Ignore if there are missing
            fields that are required.

    Returns:
        dict(str, str): The given `user` with unknown fields removed.

    Raises:
        InvalidUserError: Raised when the given `user` does not
            provide needed information for a user. This is not raised
            if `ignore_required_fields` is True.

    """
    user_fields = set(user.keys())

    if not ignore_required_fields:
        missing_required_fields = REQUIRED_FIELDS.difference(user_fields)
        if missing_required_fields:
            raise _exceptions.InvalidUserError(
                f"Missing required user fields: {missing_required_fields}"
            )

    unknown_fields = user_fields.difference(REQUIRED_FIELDS)
    if unknown_fields:
        _LOGGER.warning(f"Unknown field(s) given, discarding...: {str(unknown_fields)}")
        user = {
            required_field: field_value
            for required_field, field_value in user.items()
            if required_field in REQUIRED_FIELDS
        }

    return user


class BaseDataStore(object):
    """The base data store used to access the information for Phonebook.

    When subclassing this class the following methods must be
    implemented:

    * :meth:`read`
    * :meth:`create`
    * :meth:`update`
    * :meth:`delete`

    By default, the :meth:`get` method calls the :meth:`read` method
    with the "name" filter set. If a more efficient method of finding a
    single result is available to your data store (e.g. a database ONE
    query), the :meth:`get` method can be overloaded.

    When subclassing make sure to define the "NAME" attribute for your
    class. This attribute is used by the CLI to allow the CLI user to
    choose their backend.

    """

    def get(self, name):
        """Get a single user's information from the data store.

        Args:
            name (str): The name of the user to get from the data store.

        Returns:
            dict(str, str): The information for the requested user.

        Raises:
            MissingUserError: Raised when the requested user does not
                exist in the data store.

        """
        users = self.read(filters={"name": name})
        if not users:
            raise _exceptions.MissingUserError(
                f"Unable to find a user with '{name}' name!"
            )
        return users[0]

    @abc.abstractmethod
    def read(self, filters=None):
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

    @abc.abstractmethod
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

    @abc.abstractmethod
    def delete(self, name):
        """Delete the user with given `name` from the data store.

        Args:
            name (str): The name of the user to delete from the data
                store.

        Raises:
            MissingUserError: Raised when a user with the given `name`
                does not exist in the data store.

        """

    @abc.abstractmethod
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
