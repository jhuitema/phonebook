"""Exceptions used and raised by the Phonebook library."""


class MissingUserError(Exception):
    """User does not exist in the data store."""


class InvalidUserError(Exception):
    """User information is missing required information."""


class DuplicateUserError(Exception):
    """User with the given name already exists in the data store."""
