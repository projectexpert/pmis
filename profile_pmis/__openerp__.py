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
    'name': 'Profile PMIS',
    'version': '1.0',
    'category': 'Project Management',
    'sequence': 9,
    'summary': 'Project Management Information System',
    'description': """
Installs the dependencies needed to set up a Project Management
Information System on Odoo framework. Manual setup is needed to
set the planning accounts on products and human resources.
        """,
    'author': 'Matmoz d.o.o.',
    'website': 'http://www.matmoz.si',
    'complexity': 'easy',
    'images': [],
    'depends': [
        'project_charter',
        'analytic_line_plan_commit_hr_timesheet',
        'analytic_line_plan_commit_purchase',
        'analytic_line_plan_commit_sale',
        'analytic_resource_plan_purchase',
        'analytic_wip_report',
        'account_analytic_lob',
        'project_time_milestone',
        'project_time_schedule',
        'project_time_sequence',
        'project_wbs_task',
        'sale_order_line_analytic_search',
        'purchase_order_analytic_search',
        'account_invoice_debt_start_date',
        'crm_project_task',
        'crm_todo',
        'hr_timesheet_product',
        'matmoz_reports',
        'operations_board',
        'project_document_page',
        'project_task_issues',
        'risk_management',
        'change_management'
    ],
    'data': [],
    'test': [],
    'demo': [],
    'installable': True,
    'auto_install': False,
    'application': True,
    'license': 'AGPL-3',
}
