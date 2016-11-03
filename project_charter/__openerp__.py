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
    'version': '8.0.1.1.9',
    'author': 'Matmoz d.o.o., '
              'Project Expert Team',
    'contributors': [
        'Matjaž Mozetič <m.mozetic@matmoz.si>',
    ],
    'website': 'http://project.expert',
    'category': 'Project Management',
    'license': 'AGPL-3',
    'sequence': 9,
    'summary': 'Project Charter',
    'complexity': 'easy',
    'images': [],
    'depends': [
        'project',
        'analytic_account_sequence',
        'analytic_plan',
        'analytic_resource_plan',
        'analytic_billing_plan',
        'project_wbs',
        'web_ckeditor4',
        'document_page',
        'project_document_page',
        'document_page_approval',
    ],
    'data': ['views/project_charter_view.xml',
             'views/analytic_view.xml',
             'removed_views/project_wbs_config.xml',
             'security/ir.model.access.csv'],
    'test': [],
    'demo': [],
    'installable': True,
    'auto_install': False,
    'application': False,
}
