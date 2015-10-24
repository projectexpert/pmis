.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
    :alt: License AGPL-3

====================
Progress measurement
====================
The progress of a project indicates the degree of completion, with respect
to the estimated scope of work. Generally the progress cannot be
automatically measured and it is based on the expert judgement or the
completion of checklists that determine the degree of completion of a
project.


Define Progress Types:
----------------------
Each company can have different needs of project progress control.
It is for this reason that it is necessary to define Progress Types.
The Progress Types are entities that can be created to measure the
progress differently.
For example, a project can be measured on a percent basis, or by
quantity used of a given resource.
A Progress Type is defined by the following attributes:

* Name: Name given to the type of progress
* Maximum value: Maximum value that is permitted for the object being measured as a total measure of progress.
* Precision: Value of increments permitted for the given progress type measured as a total measure of progress.


Define Progress Measurements:
-----------------------------
Progress Measurements record the results of the measurement.
A Progress Measurement is defined by the following attributes:

* Date: When the measurement occurred
* Progress Type.
* Value: Results of the measurement. Must be defined in the precision indicated by the progress type. The user cannot enter a value that exceeds the maximum permitted value for that progress type.
* Description: description of the measurement
* Entered by: User that entered the measurement

Installation
============

* The module automatically takes care of its dependencies and is ready for use after the installation

Credits
=======

Contributors
------------

* Eficent <http://www.eficent.com>
* Matmoz d.o.o. <http://www.matmoz.si>

Maintainer
----------

.. image:: http://www.matmoz.si/wp-content/uploads/2015/10/PME.png
   :alt: Project Expert
   :target: http://project.expert

This module is maintained by Project Expert Team.

Project Expert is a joint effort between EFICENT (Barcelona, Spain) and MATMOZ (Ljubljana, Slovenia),
both active members of Odoo Community Association (OCA).

.. image:: http://odoo-community.org/logo.png
   :alt: Odoo Community Association
   :target: http://odoo-community.org

OCA, or the Odoo Community Association, is a nonprofit organization whose
mission is to support the collaborative development of Odoo features and
promote its widespread use.

