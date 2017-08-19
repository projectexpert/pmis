# -*- coding: utf-8 -*-
# Copyright 2014-17 Eficent Business and IT Consulting Services S.L.
# Copyright 2016 Matmoz d.o.o.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    'name': 'Stock Analytic Account',
    'version': '10.0.1.0.1',
    'author':   'Eficent, '
                'Project Expert Team',
    'website': 'http://project.expert',
    'category': 'Project Management',
    'license': 'AGPL-3',
    'depends': [
        'stock_analytic'
    ],
    'data': [
        'view/stock_view.xml',
        'view/stock_picking_view.xml',
        'view/analytic_account_view.xml',
    ],
    'installable': True,
}
