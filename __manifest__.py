# -*- coding: utf-8 -*-
# Copyright 2015 Eficent Business and IT Consulting Services S.L.
# (Jordi Ballester Alomar)
# Copyright 2016 Matmoz d.o.o.
# (Matjaž Mozetič)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    'name': 'Analytic Plan',
    'version': '10.0.1.0.0',
    'author':   'Eficent, '
                'Matmoz, '
                'Project Expert Team',
    'website': 'http://project.expert',
    'category': 'Project Management',
    'license': 'AGPL-3',
    'depends': [
        'account',
        'analytic',
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
    'installable': True,
}
