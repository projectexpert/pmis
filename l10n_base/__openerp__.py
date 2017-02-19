# -*- encoding: utf-8 -*-

{
    'name': 'Base Localization',
    'version': '8.0.4.1.2',
    'summary': 'Base Localization Module for sub-regions',
    'author':   'Didotech, '
                'Matmoz d.o.o.',
    'website': 'http://www.didotech.com',
    'license': "AGPL-3",
    'contributors': [
        'Matjaž Mozetič <m.mozetic@matmoz.si>',
        'Andrei Levin <andrei.levin@didotech.com>',
        'Davide Corio <davide.corio@domsense.com>',
        'Luca Subiaco <subluca@gmail.com>',
        'Simone Orsi <simone.orsi@domsense.com>',
        'Mario Riva <mario.riva@domsense.com>',
        'Mauro Soligo <mauro.soligo@katodo.com>',
        'Giovanni Barzan <giovanni.barzan@gmail.com>',
        'Lorenzo Battistini <lorenzo.battistini@domsense.com>',
        'Roberto Onnis <onnis.roberto@gmail.com>',
        'Carlo Vettore <carlo.vettore@didotech.com>'
        ],
    'depends': [
        'base',
        'crm'
    ],
    'data': [
        'views/partner_view.xml',
        'views/crm_view.xml',
        'security/ir.model.access.csv',
        'data/res.country.csv',
    ],
    'qweb': [],
    'demo': [],
    'test': [],
    'active': False,
    'installable': True
}
