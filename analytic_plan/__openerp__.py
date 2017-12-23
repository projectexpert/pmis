# -*- coding: utf-8 -*-
#    Copyright 2017 Matmoz d.o.o. & Luxim d.o.o. (Matjaž Mozetič)
#    Copyright 2015 Eficent (Jordi Ballester Alomar)
#    License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    'name': 'Analytic Plan',
    'version': '8.0.3.0.2',
    'author':   'Eficent, '
                'Matmoz, '
                'Luxim, '
                'Project Expert Team',
    'contributors': [
        'Jordi Ballester <jordi.ballester@eficent.com>',
        'Matjaž Mozetič <m.mozetic@matmoz.si>',
    ],
    'website': 'http://project.expert',
    'category': 'Advanced Project Management',
    'license': 'AGPL-3',
    'depends': ['account', 'analytic', 'project'],
    'data': [
        'data/account_analytic_plan_version_data.xml',
        'views/account_analytic_plan_version_view.xml',
        'views/account_analytic_plan_journal_view.xml',
        'views/account_analytic_line_plan_view.xml',
        'views/account_analytic_account_view.xml',
        'views/account_analytic_plan_journal_data.xml',
        'views/product_view.xml',
        'views/project_view.xml',
        'wizard/analytic_plan_copy_version.xml',
        'security/ir.model.access.csv',
    ],
    'test': [
    ],
    'installable': True,
    'active': False,
    'certificate': '',
}
