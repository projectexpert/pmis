# -*- coding: utf-8 -*-
#    Copyright 2016 MATMOZ, Slovenia (Matjaž Mozetič)
#    Copyright 2018 EFICENT (Jordi Ballester Alomar)
#    Copyright 2018 LUXIM, Slovenia (Matjaž Mozetič)
#    Together as the Project Expert Team
#    License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    'name': 'Analytic Deliverable Planning',
    'version': '10.0.1.0.0',
    'category': 'Advanced Project Management',
    'license': 'AGPL-3',
    'summary': 'Deliverable planning and sale price analysis',
    'author': 'Luxim, Eficent, Project Expert Team',
    'website': 'https://github.com/projectexpert',
    # 'author': 'Luxim, Eficent, Odoo Community Association (OCA)',
    # 'website': 'https://github.com/OCA/...',
    'contributors': [
        'Matjaž Mozetič <matjaz@luxim.si>',
    ],
    'depends': [
        'account',
        'analytic_plan',
        'analytic_resource_plan',
        'project_wbs',
        'sale_crm'
    ],
    'data': [
        'security/ir.model.access.csv',
        'view/account_analytic_plan_version_view.xml',
        'view/account_analytic_line_plan_view.xml',
        'view/analytic_deliverable_plan_view.xml',
        'view/analytic_account_view.xml',
        'view/project_view.xml',
        'view/deliverable_plan_default.xml',
        'view/resource_plan.xml',
        'wizard/analytic_deliverable_plan_copy_version_view.xml',
        'wizard/deliverable_plan_line_change_state_view.xml',
        'wizard/deliverable_plan_line_make_sale.xml',
    ],
    'installable': True,
    'application': True,
}
