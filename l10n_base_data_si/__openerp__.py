# -*- encoding: utf-8 -*-

{
    'name': 'Slovene ZIP completion list',
    'version': '8.2.0.0.1',
    'summary': 'Data import for Slovenian subregions',
    'author':   'Matmoz d.o.o., '
                'Didotech',
    'website': 'http://www.matmoz.si',
    'license': 'AGPL-3',
    'contributors': [
        'Matjaž Mozetič <m.mozetic@matmoz.si>',
    ],
    'depends': [
        'l10n_base'
    ],
    'data': [
        'data_si/res.region.csv',
        'data_si/res.province.csv',
        'data_si/res.city.csv',
        'data_si/res.partner.title.csv',
        'data_si/res.country.csv',
    ],
    'qweb': [],
    'demo': [],
    'test': [],
    'active': False,
    'installable': True
}
