# -*- coding: utf-8 -*-
# © 2017 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Stock Location in Project",
    "version": "8.0.1.0.0",
    "author": "Eficent",
    "license": 'AGPL-3',
    "website": "www.eficent.com",
    'category': 'Advanced Project Management',
    "depends": ["project_stock", "analytic_location"],
    "Summary": """
        stock location in the project.
    """,
    "data": [
        "view/project_view.xml",
        "security/ir.model.access.csv",
    ],
}
