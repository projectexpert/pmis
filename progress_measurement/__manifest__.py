# -*- coding: utf-8 -*-
# © 2014-17 Eficent Business and IT Consulting Services S.L.
# © 2016 Matmoz d.o.o.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Progress measurement",
    "version": "10.0.1.0.0",
    "author": "Eficent",
    "website": "www.eficent.com",
    "category": "Generic Modules",
    "depends": ["project"],
    "summary": """
        Project degree of completion with respect
        to the estimated scope of work
    """,
    "data": [
        "views/progress_measurement_type_view.xml",
        "security/ir.model.access.csv",
    ],
    'installable': True,
}
