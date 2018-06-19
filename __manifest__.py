# -*- coding: utf-8 -*-
# Copyright 2015 Odoo SA
# Copyright 2017 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Analytic Journal",
    "version": "9.0.1.0.0",
    "summary": "Analytic Journals as in previous Odoo versions",
    "author": "Odoo SA",
    "category": "Analytic",
    "depends": ["account", "analytic"],
    "data": ['views/analytic_view.xml',
             'security/ir.model.access.csv', ],
    'installable': True,
}
