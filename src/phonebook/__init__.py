"""A library to store and search for users, phone numbers, and addresses."""


import os


_VERSION_PATH = os.path.join(os.path.dirname(__file__), "VERSION")
with open(_VERSION_PATH) as _VERSION_FILE:
    __version__ = _VERSION_FILE.read().strip()
    """str: The version of the package."""


__all__ = ["__version__"]
