# -*- coding: utf-8 -*-
# © 2017 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    'name': 'Purchase Stock Location Analytic',
    'version': '8.0.1.0.0',
    'author': 'Eficent, '
              'Project Expert Team',
    'website': 'http://project.expert',
    'category': 'Analytic',
    'license': 'AGPL-3',
    'depends': [
        'stock_analytic_account_location',
        'purchase',
        'purchase_stock_analytic'
    ],
    'summary': 'Purchases using analytic locations',
    'installable': True,
    'auto_install': False,
}
