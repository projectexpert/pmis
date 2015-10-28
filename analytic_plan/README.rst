.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
    :alt: License AGPL-3

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
