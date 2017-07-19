# -*- coding: utf-8 -*-
# Copyright 2017 Eficent Business and IT Consulting Services S.L.
# Copyright 2017 Luxim d.o.o.
# Copyright 2017 Matmoz d.o.o.
# Copyright 2017 Deneroteam.

# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Project WBS Stage",
    "version": "9.0.1.0.0",
    "author": "Eficent",
    "website": "www.eficent.com",
    "category": "Generic Modules/Projects & Services",
    "summary": """Add the stage to the project wbs
    """,
    "depends": ["project_wbs", "analytic", "project"],
    "data": [
        "views/project_project_stage_view.xml",
        "views/project_project_view.xml",
        "security/ir.model.access.csv",
    ],

    'installable': True,
}
