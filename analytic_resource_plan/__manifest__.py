 # -*- coding: utf-8 -*-
 # Copyright 2017 Eficent Business and IT Consulting Services S.L.
 # License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    'name': 'Analytic Resource Planning',
    'version': '10.0.1.0.0',
    'author':   'Eficent, '
                'Matmoz, '
                'Luxim, '
                'Project Expert Team',
    'website': 'http://project.expert',
    'category': 'Project Management',
    'license': 'AGPL-3',
    'depends': [
        'account',
        'purchase',
        'analytic_plan',
        'analytic_resource_plan_stock'
    ],
    'data': [
        'security/ir.model.access.csv',
        'view/account_analytic_plan_version_view.xml',
        'view/analytic_resource_plan_view.xml',
        'view/analytic_account_view.xml',
        'view/product_view.xml',
        'view/project_view.xml',
        'view/resource_plan_default.xml',
        'wizard/analytic_resource_plan_copy_version_view.xml',
        'wizard/resource_plan_line_change_state_view.xml',
    ],
    'installable': True,
}
