# -*- coding: utf-8 -*-
# © 2017 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    'name': 'Update Product Qty Analytic',
    'version': '8.0.1.0.0',
    'author':   'Eficent, '
                'Project Expert Team',
    'website': 'http://project.expert',
    'category': 'Analytic',
    'license': 'AGPL-3',
    'depends': [
        'analytic',
        'stock',
        'stock_analytic_account_location'
    ],
    'summary': 'Update product Qty when using Analytic locations',
    'data': ['wizard/stock_change_product_qty.xml'],
    'installable': True,
    'auto_install': False,
}
