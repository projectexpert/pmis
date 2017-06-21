# -*- coding: utf-8 -*-
# © 2015 Eficent Business and IT Consulting Services S.L.
# (Jordi Ballester Alomar)
#
# © 2016 Matmoz d.o.o.
# (Matjaž Mozetič)
#
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    'name': 'Analytic Plan',
    'version': '8.0.2.0.1',
    'author':   'Eficent, '
                'Matmoz, '
                'Project Expert Team',
    'contributors': [
        'Jordi Ballester <jordi.ballester@eficent.com>',
        'Matjaž Mozetič <m.mozetic@matmoz.si>',
    ],
    'website': 'http://project.expert',
    'category': 'Project Management',
    'license': 'AGPL-3',
    'depends': ['account', 'analytic', 'project', 'project_wbs'],
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
