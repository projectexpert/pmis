# -*- coding: utf-8 -*-
# © 2015 Eficent Business and IT Consulting Services S.L. -
# Jordi Ballester Alomar
# © 2015 Serpent Consulting Services Pvt. Ltd. - Sudhir Arya
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Work Breakdown Structure",
    "version": "8.0.1.0.0.",
    "author": "Eficent Business and IT Consulting Services S.L., "
              "Serpent Consulting Services Pvt. Ltd.,"
              "Odoo Community Association (OCA)",
    "website": "www.eficent.com",
    "category": "Generic Modules/Projects & Services",
    "depends": ["account", "project"],
    "description": """Project Scope
    - The hierarchy of a project is considered the WBS
    (Work Breakdown Structure)
    - The analytic accounts in the project hierarchies are considered
    WBS components
    - The analytic account code is shown in the project
    - The complete WBS path code  is shown in the analytic account and
    in the project
    - The complete WBS path name is shown in the analytic account and
    in the project
    - The WBS paths are concatenated with /
    - It is possible to search projects by complete WBS path code & name
    - It is possible to search tasks by project complete WBS path code & name
    - The WBS components can be classified as project, phase, deliverable,
    work package.
    - The classification is shown in the project and analytic account views
    - A project stage attribute is incorporated in the analytic account and
    displayed in the project and analytic account views.
    """,
    'data': [
        "views/analytic_account_stage_view.xml",
        "views/account_analytic_account_view.xml",
        "views/project_project_view.xml",
        "security/ir.model.access.csv",
    ],
    'installable': True,
    'application': True,
}
