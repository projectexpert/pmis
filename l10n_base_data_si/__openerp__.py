# -*- encoding: utf-8 -*-

{
    'name': 'Slovene subregions and ZIP completion',
    'version': '8.2.0.0.2',
    'summary': 'Data import for Slovenian subregions',
    'author':   'Luxim & Matmoz',
    'website': 'https://www.luxim.si',
    'license': 'AGPL-3',
    'contributors': [
        'Matjaž Mozetič <m.mozetic@matmoz.si>',
    ],
    'depends': [
        'l10n_base'
    ],
    'data': [
        'data_si/res_region_data.xml',
        'data_si/res_province_data.xml',
        'data_si/res_city_data.xml',
        'data_si/res_country_data.xml',
    ],
    'qweb': [],
    'demo': [],
    'test': [],
    'active': False,
    'installable': True
}
