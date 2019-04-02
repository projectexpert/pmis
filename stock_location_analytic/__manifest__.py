# -*- coding: utf-8 -*-
# Copyright 2017 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    'name': 'Stock Location Analytic',
    'version': '10.0.1.0.0',
    'category': 'Logistics',
    'summary': 'Introduces the analytic account to the locations',
    'author': 'Eficent',
    "license": "AGPL-3",
    'website': 'http://www.eficent.com',
    'depends': [
        'stock',
        'analytic',
        'analytic_location'
    ],
    'data': [
        'views/stock_view.xml',
        'views/analytic_view.xml',
    ],
    'demo': [
        'demo/stock_demo.xml'
    ],
    'installable': True,
}
