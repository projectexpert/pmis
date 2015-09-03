# -*- encoding: utf-8 -*-
{
    'name': 'Matmoz Extended Reports',
    'version': '1.2.1',
    'category': 'Reports',
    'summary': 'Extended Sale Reports',
    'description': """
    Matmoz Custom Reports
    - added company VAT n. on header
    - added due date, debt date and place of issue
    """,
    'author': 'Matmoz d.o.o.',
    'website': 'http://www.matmoz.si',
    'license': "AGPL-3",
    'contributors': [
        'Matjaž Mozetič <m.mozetic@matmoz.si>',
    ],
    'depends': [
        'base_setup',
        'report',
        'account_invoice_debt_start_date',
        'sale'
    ],
    'data': [
        'views/report.external_layout_header_ext.xml',
        'views/account.report_invoice_document_ext.xml',
        'views/sale.report_saleorder_document_ext.xml',
    ],
    'demo': [],
    'installable': True,
    'auto_install': False,
    'application': False,
}
