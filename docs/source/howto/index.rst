.. _howto:

#############
How-To Guides
#############

Here you will find short answers to real-world problems with this
package. The how-to guides do not cover topics in depth, but you can
find that material in the :ref:`reference`. These guides will help you
quickly accomplish common tasks.

.. See https://documentation.divio.com/how-to-guides/ for inspiration

.. contents::
    :local:


How to Use a Different Data Store
=================================

You can use a different data store using the ``data-store`` argument:

.. code-block:: bash

    phonebook --data-store yaml read

.. note::

    Note that data entered into one data store is not transferred into
    the other.
