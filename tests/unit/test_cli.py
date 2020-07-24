"""Test the :mod:`phonebook._cli` module."""


import argparse
import copy
import json

import pytest
import sys

import phonebook._cli


@pytest.fixture(autouse=True)
def clear_sys_argv():
    """Revert sys.argv after the test."""
    orig_argv = copy.deepcopy(sys.argv)
    yield
    sys.argv = orig_argv


def test_version(mocker, capsys):
    """Test ``phonebook --version``."""
    sys.argv = ["phonebook", "--version"]

    phonebook._cli.main()
    out, err = capsys.readouterr()
    assert out.strip() == phonebook.__version__


def test_get(mocker, capsys):
    """Test ``phonebook get``."""
    sys.argv = ["phonebook", "get", "Eric Idle"]
    mock_get = mocker.patch("phonebook.get", return_value=[])

    phonebook._cli.main()

    mock_get.assert_called_once_with("Eric Idle")
    out, err = capsys.readouterr()
    assert json.loads(out) == []


def test_read_no_filters(mocker, capsys):
    """Test ``phonebook read`` without filters."""
    sys.argv = ["phonebook", "read"]
    mock_read = mocker.patch("phonebook.read", return_value=[])

    phonebook._cli.main()

    mock_read.assert_called_once_with(filters={})
    out, err = capsys.readouterr()
    assert json.loads(out) == []


def test_read_with_filters(mocker, capsys):
    """Test ``phonebook read`` with filters."""
    sys.argv = [
        "phonebook",
        "read",
        "--name",
        "name_filter",
        "--phone",
        "phone_filter",
        "--address",
        "address_filter",
    ]
    mock_read = mocker.patch("phonebook.read", return_value=[])

    phonebook._cli.main()

    mock_read.assert_called_once_with(
        filters={
            "name": "name_filter",
            "phone": "phone_filter",
            "address": "address_filter",
        }
    )
    out, err = capsys.readouterr()
    assert json.loads(out) == []


def test_create(mocker):
    """Test ``phonebook create`` with filters."""
    sys.argv = ["phonebook", "create", "Eric Idle", "999-999-9999", "Here"]
    mock_create = mocker.patch("phonebook.create")

    phonebook._cli.main()

    mock_create.assert_called_once_with(
        {"name": "Eric Idle", "phone": "999-999-9999", "address": "Here",}
    )


def test_delete(mocker):
    """Test ``phonebook delete`` with filters."""
    sys.argv = ["phonebook", "delete", "Eric Idle"]
    mock_delete = mocker.patch("phonebook.delete")

    phonebook._cli.main()

    mock_delete.assert_called_once_with("Eric Idle")


def test_update(mocker):
    """Test ``phonebook update`` with filters."""
    sys.argv = [
        "phonebook",
        "update",
        "Eric Idle",
        "--name",
        "New Name",
        "--phone",
        "New Phone",
        "--address",
        "New Address",
    ]
    mock_update = mocker.patch("phonebook.update")

    phonebook._cli.main()

    mock_update.assert_called_once_with(
        "Eric Idle", name="New Name", phone="New Phone", address="New Address",
    )
