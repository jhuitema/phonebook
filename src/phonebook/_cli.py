"""The Command Line Interface for the Phonebook."""


import argparse
import json
import logging

import yaml

import phonebook
import phonebook._datastore


_DATA_STORES = {
    data_store.NAME: data_store for data_store in phonebook._datastore.DATA_STORES
}
_OUTPUT_FORMATS = (
    "json",
    "yaml",
)


def _parse_args():
    """Create a parser for command line usage."""
    parser = argparse.ArgumentParser(
        description="Store and retrieve user, phone number, and address information."
    )

    parser.add_argument(
        "--version",
        action="store_true",
        help="Get the version of the Phonebook package.",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Increase the verbosity of the output.",
    )
    parser.add_argument(
        "--data-store",
        default=phonebook._datastore.DATA_STORES[0].NAME,
        choices=_DATA_STORES.keys(),
        help="The Data Store to use to store the backend.",
    )
    subparsers = parser.add_subparsers(title="commands", dest="command")

    # get args
    get_parser = subparsers.add_parser(
        "get", help="Get a user from the Phonebook by their name."
    )
    get_parser.add_argument(
        "name", help="The name of the user to get the information for."
    )
    get_parser.add_argument(
        "--output-format",
        default=_OUTPUT_FORMATS[0],
        choices=_OUTPUT_FORMATS,
        help="Specify the desired manner of output.",
    )

    # read args
    read_parser = subparsers.add_parser(
        "read",
        help=(
            "Get users from the Phonebook based on provided fnmatch-style filters. "
            "If no filters are given then all users will be provided."
        ),
    )
    read_parser.add_argument(
        "-n",
        "--name",
        help="The fnmatch-style name expression to use to filter the users by.",
    )
    read_parser.add_argument(
        "-p",
        "--phone",
        help="The fnmatch-style phone number expression to use to filter the users by.",
    )
    read_parser.add_argument(
        "-a",
        "--address",
        help="The fnmatch-style address expression to use to filter the users by.",
    )
    read_parser.add_argument(
        "--output-format",
        default=_OUTPUT_FORMATS[0],
        choices=_OUTPUT_FORMATS,
        help="Specify the desired manner of output.",
    )

    # create args
    create_parser = subparsers.add_parser(
        "create", help="Create a new user in the Phonebook."
    )
    create_parser.add_argument("name", help="The name of the user to create.")
    create_parser.add_argument("phone", help="The phone number of the user to create.")
    create_parser.add_argument("address", help="The address of the user to create.")

    # delete args
    delete_parser = subparsers.add_parser(
        "delete", help="Delete a user in the Phonebook."
    )
    delete_parser.add_argument("name", help="The name of the user to delete.")

    # update args
    update_parser = subparsers.add_parser(
        "update", help="Update an existing user in the Phonebook."
    )
    update_parser.add_argument(
        "user_name", help="The name of the user to update the entry of."
    )
    update_parser.add_argument("-n", "--name", help="The name to update the user with.")
    update_parser.add_argument(
        "-p", "--phone", help="The phone number to update the user with."
    )
    update_parser.add_argument(
        "-a", "--address", help="The address to update the user with."
    )

    return parser.parse_args()


def _print_result(result, output_format):
    """Print the result to the terminal."""
    if output_format == "json":
        output = json.dumps(result, indent=2)
    elif output_format == "yaml":
        output = yaml.dump(result, default_flow_style=False, indent=2)
    print(output)


def _handle_get(args):
    """Output the result of the "get" command."""
    result = phonebook.get(args.name)
    _print_result(result, args.output_format)


def _handle_read(args):
    """Output the result of the "read" command."""
    filters = {}
    if args.name:
        filters["name"] = args.name
    if args.phone:
        filters["phone"] = args.phone
    if args.address:
        filters["address"] = args.address

    result = phonebook.read(filters=filters)
    _print_result(result, args.output_format)


def _handle_create(args):
    """Add an entry to the Phonebook."""
    phonebook.create({"name": args.name, "phone": args.phone, "address": args.address})


def _handle_delete(args):
    """Delete an entry to the Phonebook."""
    phonebook.delete(args.name)


def _handle_update(args):
    """Update an entry in the Phonebook."""
    user_fields = {}
    if args.name:
        user_fields["name"] = args.name
    if args.phone:
        user_fields["phone"] = args.phone
    if args.address:
        user_fields["address"] = args.address

    phonebook.update(args.user_name, **user_fields)


def main():
    """The main entry point for the CLI."""
    args = _parse_args()

    level = logging.INFO
    format_str = "%(levelname)s - %(message)s"
    if args.verbose:
        level = logging.DEBUG
        format_str = "%(asctime)s %(levelname)s - %(message)s"
    logging.basicConfig(
        level=level, format=format_str, handlers=[logging.StreamHandler()]
    )

    if args.version:
        print(phonebook.__version__)
        return 0

    data_store = _DATA_STORES[args.data_store]()
    phonebook.set_data_store(data_store)

    command_funcs = {
        "get": _handle_get,
        "read": _handle_read,
        "create": _handle_create,
        "delete": _handle_delete,
        "update": _handle_update,
    }
    command_funcs[args.command](args)

    return 0
