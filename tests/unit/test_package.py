"""Tests for the phonebook module."""


import importlib
import pkgutil

import phonebook


def test_version():
    """Test the `__version__` exists."""
    assert hasattr(phonebook, "__version__")
    assert phonebook.__version__


def test_imports():
    """Test the submodules all import."""
    package = phonebook
    prefix = package.__name__ + "."
    for _, modname, _ in pkgutil.walk_packages(package.__path__, prefix):
        importlib.import_module(modname)
