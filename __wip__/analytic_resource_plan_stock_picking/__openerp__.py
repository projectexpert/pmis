# -*- coding: utf-8 -*-
# © 2017 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Analytic Resource Planning - get resources",
    "version": "8.0.1.0.0",
    "author": "Eficent",
    "license": 'AGPL-3',
    "website": "www.eficent.com",
    "category": "Generic Modules/Projects & Services",
    "depends": ["analytic_resource_plan", "analytic_location",
                "purchase_request", "project_location"],
    "description": """
        Fetch stock for projects
    """,
    "data": [
        "views/stock_picking_view.xml",
        "views/analytic_resource_plan_view.xml",
    ],
    'installable': True,
}
