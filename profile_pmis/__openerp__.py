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
    'version': '8.0.1.1.4',
    'sequence': 9,
    'summary': 'Project Management Information System',
    'author':   'Matmoz d.o.o., '
                'Project Expert Team',
    'contributors': [
        'Matjaž Mozetič <m.mozetic@matmoz.si>',
    ],
    'website': 'http://project.expert',
    'category': 'Project Management',
    'license': 'AGPL-3',
    'complexity': 'easy',
    'images': [],
    'depends': [
        'project_charter',
        'account_invoice_debt_start_date',
        'account_report_dept_start_date',
        'analytic_account_sequence',
        'account_analytic_lob',
        'analytic_billing_plan',
        'analytic_location',
        'analytic_resource_plan_purchase_request',
        'analytic_resource_plan_stock',
        'analytic_wip_report',
        'analytic_schedule',
        'change_management',
        'crm_change_request',
        'crm_project',
        'crm_todo',
        'gantt_improvement',
        'hr_timesheet_product',
        'issue_change_request',
        'operations_board',
        'project_document_page',
        'project_events',
        'project_hr_stakeholder',
        'project_meetings',
        'project_task_issues',
        'project_time_easy_scheduling',
        'project_time_milestone',
        'project_time_schedule',
        'project_time_sequence',
        'project_wbs_task',
        'risk_management',
        'purchase_request_to_rfq',
        'stock_analytic_account',
        'web_sheet_full_width',
        'web_dialog_size',
        'web_export_view',
        'web_advanced_search_x2x',
        # 'analytic_line_plan_commit_hr_timesheet',
        # 'analytic_line_plan_commit_purchase',
        # 'analytic_line_plan_commit_sale',
        # 'purchase_order_analytic_search',
        # 'sale_order_line_analytic_search',
    ],
    'data': [],
    'test': [],
    'demo': [],
    'installable': True,
    'auto_install': False,
    'application': True,
}
