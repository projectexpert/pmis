{
    'name': 'Show hr_timesheet product',
    'version': '0.1',
    'category': 'HR',
    'summary': 'HR',
    'description': """
    Display the otherwise hidden product_id in timesheet lines.
    """,
    'author': 'Matmoz d.o.o.',
    'website': 'http://www.matmoz.si',
    'depends': ['hr_timesheet'],
    'data': [
        'views/hr_timesheet_product.xml',
    ],
    'demo': [],
    'installable': True,
    'auto_install': False,
    'application': False,
}
