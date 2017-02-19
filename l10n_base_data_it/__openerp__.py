# -*- encoding: utf-8 -*-

{
    'name': 'Italian ZIP completion',
    'version': '8.2.0.0.1',
    'summary': 'Data import for Italian subregions',
    'author':   'Didotech, '
                'Matmoz d.o.o.',
    'website': 'http://www.didotech.com',
    'license': 'AGPL-3',
    'contributors': [
        'Andrei Levin <andrei.levin@didotech.com>',
        'Carlo Vettore <carlo.vettore@didotech.com>'
        'Matjaž Mozetič <m.mozetic@matmoz.si>',
        ],
    'depends': [
        'l10n_base'
    ],
    'data': [
        'data_it/res.region.csv',
        'data_it/res.province.csv',
        'data_it/res.city.csv',
        'data_it/res.country.csv',
    ],
    'qweb': [],
    'demo': [],
    'test': [],
    'active': False,
    'installable': True
}
