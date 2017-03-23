# -*- coding: utf-8 -*-

{
    'name': 'Analytic billing plan',
    'version': '8.0.2.0.2',
    'author':   'Eficent, '
                'Matmoz, '
                'Luxim, '
                'Project Expert Team',
    'contributors': [
        'Jordi Ballester <jordi.ballester@eficent.com>',
        'Matjaž Mozetič <m.mozetic@matmoz.si>',
    ],
    'website': 'http://project.expert',
    'category': 'Project Management',
    'license': 'AGPL-3',
    'depends': [
        'account',
        'sale',
        'analytic_plan'
    ],
    'data': [
        'wizard/analytic_billing_plan_line_make_sale.xml',
        'views/analytic_billing_plan_view.xml',
        'views/analytic_account_view.xml',
        'views/product_view.xml',
        'views/project_view.xml',
        'security/ir.model.access.csv',

    ],
    'demo': [

    ],
    'test': [
    ],
    'installable': False,
    'active': False,
    'certificate': '',
}
