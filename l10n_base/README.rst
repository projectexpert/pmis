.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
    :alt: License AGPL-3

Base Localisation
=================

Project Scope
-------------

The traditional location management in Odoo expects the regional localization
done in separate efforts - each country sets its way of handling the
sub-regions (regions, provinces,states), which is good enough from a local
point of view.

When Odoo is used by a company handling partners globally, it needs a "global"
way of handling those sub-regions.

The l10n_base module provides a framework, that sets the sub-regions and
implements the auto-completion on partners, company and leads on zip or city.
The l10n_base_<country_code> sets of modules provide the sub-region data for
single countries, where several of them can be installed on the same database,
providing sub-regions for all of them on the single instance.

Installation
============

* The module automatically takes care of its dependencies and is ready for use after the installation

Credits
=======

Contributors
------------

* Matmoz d.o.o. <http://www.matmoz.si>
* Didotech S.r.l. <http://www.didotech.com>
* Luxim d.o.o. <https://www.luxim.si/>

Maintainer
----------

.. image:: https://www.pmisuite.com/wp-content/uploads/2017/06/cropped-pmisuite-full-300x300.png
   :alt: PMISuite
   :target: https://www.pmisuite.com

This module is maintained by PMISuite.com.

PMISuite is an effort started by LUXIM, a Project Management consultancy
company, Cloud Provider and Software development company from Slovenia.
