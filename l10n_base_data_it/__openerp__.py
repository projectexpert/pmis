# -*- encoding: utf-8 -*-

{
    'name': 'Italian subregions and ZIP completion',
    'version': '8.2.0.0.2',
    'summary': 'Data import for Italian subregions',
    'author':   'Didotech, '
                'Luxim & Matmoz',
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
        'data_it/res_region_data.xml',
        'data_it/res_province_data.xml',
        # 'data_it/res_city_data.xml',
        'data_it/res_country_data.xml',
    ],
    'post_init_hook': 'post_init',
    'qweb': [],
    'demo': [],
    'test': [],
    'active': False,
    'installable': True
}
