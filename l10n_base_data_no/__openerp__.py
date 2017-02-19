# -*- encoding: utf-8 -*-

{
    'name': 'Norwegian ZIP completion list',
    'version': '8.2.0.0.1',
    'summary': 'Data import for Norwegian subregions',
    'author': 'Matmoz d.o.o.',
    'website': 'http://www.matmoz.si',
    'license': 'AGPL-3',
    'contributors': [
        'Matjaž Mozetič <m.mozetic@matmoz.si>',
    ],
    'depends': [
        'l10n_base'
    ],
    'data': [
        'data_no/res.region.csv',
        'data_no/res.province.csv',
        'data_no/res.city.csv',
        'data_no/res.country.csv',
    ],
    'qweb': [],
    'demo': [],
    'test': [],
    'active': False,
    'installable': True
}
