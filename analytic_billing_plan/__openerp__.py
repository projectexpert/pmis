# -*- coding: utf-8 -*-
#    Copyright 2015 Matmoz d.o.o. (Matjaž Mozetič)
#    Copyright 2015 Eficent (Jordi Ballester Alomar)
#    Copyright 2017 Luxim d.o.o. (Matjaž Mozetič)
#    License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    'name': 'Analytic billing plan',
    'version': '8.0.2.0.5',
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
        'analytic_plan',
        'analytic_resource_plan'
    ],
    'data': [
        'wizard/analytic_billing_plan_line_make_sale.xml',
        'views/analytic_billing_plan_view.xml',
        'views/analytic_account_view.xml',
        'views/product_view.xml',
        'views/project_view.xml',
        'views/resource_plan.xml',
        'security/ir.model.access.csv',

    ],
    'demo': [

    ],
    'test': [
    ],
    'installable': True,
    'active': False,
    'certificate': '',
}
