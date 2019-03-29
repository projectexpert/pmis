# -*- coding: utf-8 -*-
#    Copyright 2016 MATMOZ, Slovenia (Matjaž Mozetič)
#    Copyright 2018 EFICENT (Jordi Ballester Alomar)
#    Copyright 2018 LUXIM, Slovenia (Matjaž Mozetič)
#    Together as the Project Expert Team
#    License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    'name': 'Analytic Plan',
    'version': '11.0.1.0.0',
    'category': 'Advanced Project Management',
    'license': 'AGPL-3',
    'summary': 'Core analytic planning module',
    'website': 'https://github.com/projectexpert',
    'author': 'Eficent, '
              'Luxim, '
              'Project Expert Team',
    # 'author': 'Eficent, '
    #           'Luxim, '
    #           'Odoo Community Association (OCA)',
    # 'website': 'https://github.com/OCA/...',
    'contributors': [
        'Matjaž Mozetič <matjaz@luxim.si>',
        'Jordi Ballester <jordi.ballester@eficent.com>',
    ],
    'depends': [
        'account',
        'analytic',
        'analytic_journal',
        'project',
        'project_wbs'
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/account_analytic_plan_version_data.xml',
        'views/account_analytic_plan_version_view.xml',
        'views/account_analytic_plan_journal_view.xml',
        'views/account_analytic_line_plan_view.xml',
        'views/account_analytic_account_view.xml',
        'views/account_analytic_plan_journal_data.xml',
        'views/product_view.xml',
        'views/project_view.xml',
        'wizard/analytic_plan_copy_version.xml',
    ],
    'installable': False,
}
