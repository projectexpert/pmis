# -*- coding: utf-8 -*-
{
    'name': 'Show hr_timesheet product',
    'version': '8.0.1.0.1',
    'summary': 'Display the otherwise hidden product_id in timesheet lines.',
    'author':   'Matmoz d.o.o., '
                'Project Expert Team',
    'contributors': [
        'Matjaž Mozetič <m.mozetic@matmoz.si>',
    ],
    'website': 'http://project.expert',
    'category': 'Project Management',
    'license': 'AGPL-3',
    'depends': ['hr_timesheet'],
    'data': [
        'views/hr_timesheet_product.xml',
    ],
    'demo': [],
    'installable': True,
    'auto_install': False,
    'application': False,
}
