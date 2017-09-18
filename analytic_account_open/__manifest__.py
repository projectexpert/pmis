# -*- coding: utf-8 -*-
# Copyright 2014-17 Eficent Business and IT Consulting Services S.L.
# Copyright 2016 Matmoz d.o.o.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    'name': 'Analytic Account Cost Category',
    'version': '10.0.1.0.0',
    'summary': 'Adds the cost category to analytic accounts.',
    'author': 'Eficent, '
              'Project Expert Team',
    'website': 'http://project.expert',
    'category': 'Project Management',
    'license': 'AGPL-3',
    'depends': [
        'account',
        'analytic'
    ],
    'data': [
        'wizards/analytic_account_open_view.xml',
    ],
    'installable': True,
}
