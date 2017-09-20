# -*- coding: utf-8 -*-
# Copyright 2017 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    'name': 'Analytic Plan-Actual Analysis',
    'version': '10.0.1.1.0',
    'author':   'Eficent, '
                'Project Expert Team',
    'website': 'http://project.expert',
    'category': 'Project Management',
    'license': 'AGPL-3',
    'depends': [
        'analytic_plan'
    ],
    'data': [
        'security/ir.model.access.csv',
        'report/account_analytic_plan_actual_view.xml',
    ],
    'installable': True,
    'active': False,
}
