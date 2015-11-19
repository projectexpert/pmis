.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
    :alt: License AGPL-3

=======================
Project Time Management
=======================

ACTIVITY SCHEDULING

* The user accesses from Project - Project – Tasks to the list of tasks
  and milestones.

* A new tab 'Scheduling' appears under Other Info. This tab displays
  attributes relating to the task scheduling.

* The network diagram is first determined, based on the relationships
  between activities.

* Starting from the first activity identified, the network goes forward
  first to determine the early dates of tasks, taking into account the
  task durations, limitations imposed start date of tasks or actual start
  date.

* Starting from the last activity identified, the network is executed
  backwards to determine the late date, taking into account the task
  durations, limitations to date of completion of the work or the actual
  end dates.

* For those tasks that are in the critical path of the network indicator
  is marked 'Is in the Critical Path

* The Total Margin (Total float) and Free margin (Free Float) is
  determined.

* The method used is the Critical Chain Method
  (http://en.wikipedia.org/wiki/Critical_Path_Method).

* The method is calculated taking into account an existing algorithm,
  similar to the following existing code:
  (http://www.codeproject.com/KB/recipes/CriticalPathMethod.aspx).

* The critical path is calculated using the Dijkstra algorithm

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

