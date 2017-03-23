# -*- encoding: utf-8 -*-
{
    'name': 'Dept start date on sale reports and invoices',
    'version': '8.0.2.0.2',
    'category': 'Accounting',
    'summary': 'VAT n., due date, debt date and place of issue on invoice',
    'author':   'Matmoz d.o.o., '
                'Project Expert Team',
    'website': 'http://project.expert',
    'license': 'AGPL-3',
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
    ],
    'demo': [],
    'installable': False,
    'auto_install': False,
    'application': False,
}
