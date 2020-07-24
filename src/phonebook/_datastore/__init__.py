"""Functionality related to storing and retrieving user information."""


from .json_ import JSONDataStore
from .yaml_ import YAMLDataStore


DATA_STORES = (JSONDataStore, YAMLDataStore)
"""tuple: The supported data stores for Phonebook."""
