# -*- coding: utf-8 -*-
# © 2014-17 Eficent Business and IT Consulting Services S.L.
# © 2016 Matmoz d.o.o.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).


{
    'name': 'Stock Location in Analytic Account',
    'version': '9.0.1.0.0',
    'author':   'Eficent, '
                'Project Expert Team, '
                'Odoo Community Association (OCA)',
    'contributors': [
        'Jordi Ballester <jordi.ballester@eficent.com>',
        'Matjaž Mozetič <m.mozetic@matmoz.si>',
    ],
    'website': 'http://project.expert',
    'category': 'Project Management',
    'license': 'AGPL-3',
    'depends': ['analytic', 'stock', 'stock_analytic_account'],
    'data': [
        'view/analytic_account_view.xml',
    ],
    'installable': False,
    'active': False,
    'application': True,
}
