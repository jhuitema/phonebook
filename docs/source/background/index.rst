.. _background:

##########
Background
##########

Here you’ll find information related to why this package exists. This
page will explain the main use cases and the decisions made to get to
this point. This page will also explain the reliance on other libraries
and potential alternatives.

.. See https://documentation.divio.com/explanation/ for inspiration

*******
Genesis
*******

This package was created as a toy project to demonstrate my skills.


*********
Use Cases
*********

This package is made to manage user entries containing the following:

* name
* phone number
* address

The package supports adding, removing, and updating records. The package
also allows querying the added users using a simple filter syntax. The
package provides adding, removing, updating, and filtering records
through both the CLI and the API.

The package supports serializing the user data in multiple formats: JSON
and YAML.

The output of the CLI is displayed in 2 or more output formats: JSON and
YAML.
