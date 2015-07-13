# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Addons modules by MATMOZ d.o.o.
#    Copyright (C) 2015-TODAY MATMOZ d.o.o. (<http://www.matmoz.si>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

{
    'name': 'Project Charter',
    'version': '1.0',
    'category': 'Project Management',
    'sequence': 9,
    'summary': 'Project Charter',
    'description':
        """
Customizes the PM UI to follow the pmbok and iso 21500
document Project Charter, with all it's contents:
    - project charter
    - project description (with ckeditor4)
    - project scope
    - project boundaries, assumptions and constraints
    - project stakeholders
    - resource and billing plan
        """,
    'author': 'Matmoz d.o.o.',
    'website': 'http://www.matmoz.si',
    'complexity': 'easy',
    'images': [],
    'depends': [
        'project',
        'project_hr_stakeholder',
        'analytic_account_sequence',
        'analytic_plan',
        'analytic_resource_plan',
        'analytic_billing_plan',
        'project_wbs',
        'web_ckeditor4'
    ],
    'data': ['project_charter_view.xml',
             'removed_views/stakeholders_notebook.xml',
             'security/ir.model.access.csv'],
    'test': [],
    'demo': [],
    'installable': True,
    'auto_install': False,
    'application': False,
    'license': 'AGPL-3',
}
