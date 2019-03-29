.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
    :alt: License AGPL-3
    :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html

=============
Analytic Plan
=============

An effective planning of costs and revenues associated to projects or to
other analytic accounts becomes essential in organizations that are run
by projects, or profit center accounting. The process of cost planning
generally follows an rolling wave planning approach, in which the level
of detail of the planned costs is increases over time, as the details of
the work required are known to the planning group.

The module 'Analytic Plan' provides the foundation for the planning of
analytic costs and revenues, and it is used by other modules that can
originate planned costs or revenues during the business process execution.

Define Planning Versions:
-------------------------
Organizations typically maintain different versions of their planned
costs (rough cut, detailed, approved budget, committed,...).
A Planning Version is defined by the following attributes:

* Name
* Code
* Active: The planning version is active for use in the cost planning
* Default version for committed costs: This planning version should be
  used for committed costs
* Default planning version: This version is proposed by default

Define Analytic Planning Journals:
----------------------------------
The Analytic Planning Journal serves as an attribute to classify the
costs or revenue by the it's origin. It is equivalent to the Analytic
Journal.


Define Analytic Planning Lines:
-------------------------------
The analytic planning lines are used to capture the planned cost or
revenue, for a given planning version. They are equivalent to the
analytic lines, used to capture the actual cost or revenue.

Changes to the Analytic Account:
--------------------------------
The analytic account incorporates new analytic account planning attributes:

* Cumulated planned costs. Adds up all the planned costs of this
  analytic account as well as the child analytic accounts.
* Cumulated planned revenues. Adds up all the planned revenues of this
  analytic account as well as the child analytic accounts.
* Cumulated balance. Provides the difference between cumulated costs
  and revenues.

The attributes are calculated, for an analytic account, based on the
planning analytic journal lines and based on the active planning version
defined on that analytic account.

Users with permissions to access to analytic accounts can navigate from
the analytic account to the to the associated Analytic Planning Lines.

Bug Tracker
===========

Bugs are tracked on `GitHub Issues
<https://github.com/projectexpert/pmis/issues>`_. In case of trouble, please
check there if your issue has already been reported. If you spotted it first,
help us smash it by providing detailed and welcomed feedback.

Credits
=======

Contributors
------------

* Eficent <http://www.eficent.com>
* Matmoz d.o.o. <http://www.matmoz.si>
* Luxim d.o.o. <https://www.luxim.si>


Maintainer
----------

.. image:: https://avatars3.githubusercontent.com/u/15308657?s=200&v=4
   :alt: Project Expert
   :target: https://github.com/projectexpert/

This module is maintained by Project Expert Team.

Project Expert is a joint effort between EFICENT (Barcelona, Spain) and MATMOZ
(Ljubljana, Slovenia), both active members of Odoo Community Association (OCA).
Since 2017 the development team was joined by LUXIM (Nova Gorica, Slovenia)
after MATMOZ and LUXIM began the company merging process.

.. image:: http://odoo-community.org/logo.png
   :alt: Odoo Community Association
   :target: http://odoo-community.org

OCA, or the Odoo Community Association, is a nonprofit organization whose
mission is to support the collaborative development of Odoo features and
promote its widespread use.
