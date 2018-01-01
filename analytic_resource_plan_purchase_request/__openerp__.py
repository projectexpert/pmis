# -*- coding: utf-8 -*-
#    Copyright 2017 Matmoz d.o.o. (Matjaž Mozetič)
#    Copyright 2017 Eficent (Jordi Ballester Alomar)
#    Copyright 2017 Luxim d.o.o. (Matjaž Mozetič)
#    License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    'name': 'Analytic Resource Planning - Purchase Requests',
    'version': '8.0.1.0.1',
    'author':   'Eficent, '
                'Project Expert Team',
    'contributors': [
        'Jordi Ballester <jordi.ballester@eficent.com>',
        'Matjaž Mozetič <m.mozetic@matmoz.si>',
    ],
    'website': 'http://project.expert',
    'category': 'Advanced Project Management',
    'license': 'AGPL-3',
    'depends': [
        'analytic_resource_plan',
        # 'analytic_resource_plan_stock_picking',
        'analytic_location',
        'purchase_request'
    ],
    'data': [
        'views/analytic_resource_plan_line_make_purchase_request.xml',
        'views/purchase_request_view.xml',
        'views/analytic_resource_plan_view.xml',
    ],
    'demo_xml': [],
    'test': [],
    'installable': True,
    'active': False,
    'certificate': '',
}
