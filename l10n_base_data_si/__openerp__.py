# -*- encoding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2014 Didotech Srl - OpenERP 7 migration by Matmoz d.o.o.
#    $Id$
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
{
    'name': 'Slovene Localization - Base',
    'version': '2.0.0.1',
    'category': 'Localization/Slovenia',
    'description': """Slovene Localization module - Base version

Funcionalities:

- Slovenia's Statistical Regions, Municipalities, zip codes


""",
    'author':   'Matmoz d.o.o., '
                'Didotech',
    'website': 'http://www.matmoz.si',
    'license': "AGPL-3",
    'contributors': [
        'Matjaž Mozetič <m.mozetic@matmoz.si>',
    ],
    "depends": [
        'l10n_base'
    ],
    "data": [
        'data_si/res.region.csv',
        'data_si/res.province.csv',
        'data_si/res.city.csv',
        'data_si/res.partner.title.csv',
        'data_si/res.country.csv',
    ],
    "demo": [],
    "active": False,
    "installable": True
}

# http://www.istat.it/strumenti/definizioni/comuni/
# i dati dovrebbero essere sincronizzati con questi
