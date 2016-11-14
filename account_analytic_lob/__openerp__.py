# -*- coding: utf-8 -*-

{
    'name': 'Account Analytic Line of Business',
    'version': '8.0.1.0.1',
    'summary': 'Introduce business segments in analytic accounts.',
    'author':   'Eficent, '
                'Project Expert Team',
    'contributors': [
        'Jordi Ballester <jordi.ballester@eficent.com>',
        'Matjaž Mozetič <m.mozetic@matmoz.si>',
    ],
    'website': 'http://project.expert',
    'category': 'Project Management',
    'license': 'AGPL-3',
    'depends': ['account', 'analytic', 'project_wbs'],
    'data': [
        'security/ir.model.access.csv',
        'views/account_analytic_lob_view.xml',
        'views/project_view.xml',
    ],
    'demo': [

    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
