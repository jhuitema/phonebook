.. _getting_started:

###############
Getting Started
###############

These tutorials will allow you to get started using this library. They
will go step-by-step through the process of using the package for a
variety of scenarios.

.. See https://documentation.divio.com/tutorials/ for inspiration

.. contents::
    :local:


Installation
============

To install the package we can use pip:

.. This won't actually work since the package isn't on PyPI but it's nice to show the ideal :)

.. code-block:: bash

    pip install phonebook


Command Line Interface
======================

This tutorial will help you learn how to use the default data store of
the Phonebook package with the Command-Line interface.


Populate the Data Store
-----------------------

In order to actually make use of Phonebook, we first need to add some
user records! Let's begin by adding 3 records:

.. code-block:: bash

    phonebook create "Eric Idle" "123-456-7890" "there"
    phonebook create "John Cleese" "111-222-3333" "here"
    phonebook create "Terry Gilliam" "555-555-5555" "not here"


Accessing the User Records
--------------------------

Now that we've added some user records, we can start using them. There
are two main ways to access the information in Phonebook: `get` and
`read`


get
^^^

We can use the ``get`` command to get the information for a single user:

.. code-block:: bash

    phonebook get "Eric Idle"

.. code-block:: json

    {
      "name": "Eric Idle",
      "phone": "123-456-7890",
      "address": "there"
    }


read
^^^^

We can use the ``read`` command to get the information for all users:

.. code-block:: bash

    phonebook read

.. code-block:: json

    [
      {
        "name": "Eric Idle",
        "phone": "123-456-7890",
        "address": "there"
      },
      {
        "name": "John Cleese",
        "phone": "111-222-3333",
        "address": "here"
      },
      {
        "name": "Terry Gilliam",
        "phone": "555-555-5555",
        "address": "not here"
      }
    ]


We can also use the ``read`` command to filter the results:

.. code-block:: bash

    phonebook read --name "*e" --phone "1*"

.. code-block:: json

    [
      {
        "name": "Eric Idle",
        "phone": "123-456-7890",
        "address": "there"
      },
      {
        "name": "John Cleese",
        "phone": "111-222-3333",
        "address": "here"
      }
    ]

.. note::

    Note that the filter arguments ALL must be valid for a record for
    the record to be returned.


Updating A User Record
----------------------

Oh no! We got Terry's phone number wrong! It's supposed to be
`999-999-9999`. Let's fix that:

.. code-block:: bash

    phonebook update "Terry Gilliam" --phone "999-999-9999"

And just to make sure all went well let's get Terry's record again:

.. code-block:: bash

    phonebook get "Terry Gilliam"

.. code-block:: json

    {
      "name": "Terry Gilliam",
      "phone": "999-999-9999",
      "address": "not here"
    }


Deleting a User Record
----------------------

It's at this point in the story that John Cleese is leaving us. It's
time to remove him from the Phonebook as well:

.. code-block:: bash

    phonebook delete "John Cleese"


Conclusion
----------

Now the circus is closed and we come to the end of our tutorial. Now
let's recap what we've learned:

* We created new records using ``phonebook create``
* We viewed an individual record using ``phonebook get``
* We looked at all the records using ``phonebook read``
* We filtered the returned records using ``phonebook read {args}``
* We fixed an incorrect record using ``phonebook update``
* We removed a record using ``phonebook delete``


Python Library
==============

This tutorial will help you learn how to use the default data store of
the :mod:`phonebook` module.


Populate the Data Store
-----------------------

In order to actually make use of Phonebook, we first need to add some
user records! Let's begin by adding 3 records with the
:func:`phonebook.create` function:

.. code-block:: python

    phonebook.create({"name": "Eric Idle", "phone": "123-456-7890", "address": "there"})
    phonebook.create({"name": "John Cleese", "phone": "111-222-3333", "address": "here"})
    phonebook.create({"name": "Terry Gilliam", "phone": "555-555-5555", "address": "not here"})


Accessing the User Records
--------------------------

Now that we've added some user records, we can start using them. There
are two main ways to access the information in Phonebook: `get` and
`read`


get
^^^

We can use the :func:`phonebook.get` function to get the information for
a single user:

.. code-block:: python

    user = phonebook.get("Eric Idle")
    print(user)

.. code-block:: json

    {
      "name": "Eric Idle",
      "phone": "123-456-7890",
      "address": "there"
    }


read
^^^^

We can use the :func:`phonebook.read` function to get the information
for all users:

.. code-block:: python

    users = phonebook.read()
    print(users)

.. code-block:: json

    [
      {
        "name": "Eric Idle",
        "phone": "123-456-7890",
        "address": "there"
      },
      {
        "name": "John Cleese",
        "phone": "111-222-3333",
        "address": "here"
      },
      {
        "name": "Terry Gilliam",
        "phone": "555-555-5555",
        "address": "not here"
      }
    ]


We can also use the :func:`phonebook.read` function to filter the
results:

.. code-block:: python

    users = phonebook.read(filters={"name": "*e", "phone": "1*"})
    print(users)

.. code-block:: json

    [
      {
        "name": "Eric Idle",
        "phone": "123-456-7890",
        "address": "there"
      },
      {
        "name": "John Cleese",
        "phone": "111-222-3333",
        "address": "here"
      }
    ]

.. note::

    Note that the filter arguments ALL must be valid for a record for
    the record to be returned.


Updating A User Record
----------------------

Oh no! We got Terry's phone number wrong! It's supposed to be
`999-999-9999`. Let's fix that with the :func:`phonebook.update`
function:

.. code-block:: python

    phonebook.update("Terry Gilliam", phone="999-999-9999")

And just to make sure all went well let's get Terry's record again:

.. code-block:: python

    user = phonebook.get("Terry Gilliam")
    print(user)

.. code-block:: json

    {
      "name": "Terry Gilliam",
      "phone": "999-999-9999",
      "address": "not here"
    }


Deleting a User Record
----------------------

It's at this point in the story that John Cleese is leaving us. It's
time to remove him from the Phonebook as well with the
:func:`phonebook.delete` function:

.. code-block:: python

    phonebook.delete("John Cleese")


Conclusion
----------

Now the circus is closed and we come to the end of our tutorial. Now
let's recap what we've learned:

* We created new records using :func:`phonebook.create`
* We viewed an individual record using :func:`phonebook.get`
* We looked at all the records using :func:`phonebook.read`
* We used the ``filters`` argument to filter the returned records of
  :func:`phonebook.read`
* We fixed an incorrect record using :func:`phonebook.update`
* We removed a record using :func:`phonebook.delete`
