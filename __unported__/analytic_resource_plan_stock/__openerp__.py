# -*- coding: utf-8 -*-
{
    'name': 'Analytic Resource Plan Stock',
    'version': '8.0.1.0.0',
    'author':   'Eficent, '
                'Project Expert Team',
    'contributors': [
        'Jordi Ballester <jordi.ballester@eficent.com>',
        'Matjaž Mozetič <m.mozetic@matmoz.si>',
    ],
    'website': 'http://project.expert',
    'category': 'Project Management',
    'license': 'AGPL-3',
    'summary': 'Stock on Resource Plan',
    'depends': [
        'analytic_resource_plan',
        'stock'
    ],
    'data': [
        'views/analytic_resource_plan_line_view.xml'
    ],
    'test': [
    ],
    'installable': True,
    'active': False,
    'certificate': '',
}
