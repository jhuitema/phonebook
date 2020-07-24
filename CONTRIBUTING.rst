Before We Begin
===============

To work with this repository you will need to be able to run the
following:

.. code-block:: bash

    dot (from graphviz package)
    make
    python3.6
    python3.7
    python3.8
    tox
    virtualenv


Getting Started
===============

This repository comes with a Makefile that provides convenient commands
for contributors of this repository. To see a list of available targets
you can run `make help`.


Installing Locally
------------------

You can install a local copy to your machine with:

.. code-block:: bash

    make dev

This will create a local virtualenv and do a develop install. You can
now import `phonebook` in an interactive python
shell to use it.

If you just wish to build a virtualenv you can use the following:

.. code-block:: bash

    make venv


Testing
-------

The test environment is set up with tox and run by pytest.

To set up the testing environment and run the tests, use:

.. code-block:: bash

    make test

Running tests will generate a coverage report which can be viewed with:

.. code-block:: bash

    make cov

This will also run the tests in order to generate the report, if
necessary. A web browser is then launched to display the HTML report.


Building Documentation
----------------------

You can manually build the sphinx documentation with:

.. code-block:: bash

    # Build sphinx docs locally
    make doc

    # Preview local docs in browser
    make show-doc

    # Publish local docs to SITE and devpi
    make dist-doc


Contributing
============

Development in this package follows the `Git Flow`_ workflow. In
particular, all contributions must be made in their own branch, off the
`develop` branch. Upon merging back into `develop`, `develop` should
then be merged with `master` in preparation for releasing a new version
of the package.

When contributing to this repository, please first discuss the change
you wish to make via a ticket, email, or any other method with the
owners of this repository.


Linting
-------

This project follows the DNEG coding standards. Please use black and
pipe-lint to maintain style with DNEG coding standards. You can
autoformat all python source code with:

.. code-block:: bash

    make format

You can lint all python source code with:

.. code-block:: bash

    make lint


Deployment
==========

**Only members of the Pipe Core team may release a new version of this
package.** If you are not a member of Pipe Core, please ask them to
release your change, following code review approval.

First, the following files need to be updated in a separate release
commit:

- `release_notes.rst`: Update the release notes.
- `VERSION`: Update the version number.

.. code-block:: bash

    git add release_notes.rst VERSION
    git commit -m "Version X.Y.Z"
    git push

In accordance with `Git Flow`_, all releases must happen from the
`master` branch. At this point, merge `develop` into `master`. The new
version can then be released with the `dist` makefile target.

.. code-block:: bash

    git checkout master
    git merge develop
    git push
    make dist

**When you've finished with the deployment process, the `develop` and
`master` branches should be pointing to the same commit.**


Versioning
==========

We use `Semantic Versioning`_ for versioning this repository. For the
versions available, see the tags on this repository.


.. _Git Flow: https://nvie.com/posts/a-successful-git-branching-model/
.. _Semantic Versioning: https://semver.org/
