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
    'name': 'Norwegian Localization - Base',
    'version': '2.0.0.1',
    'category': 'Localization/Norway',
    'description': """Norwegian Localization module - Base version

Funcionalities:

- Data import for Norway's Provinces, Municipalities, zip codes


""",
    'author': 'Matmoz d.o.o.',
    'website': 'http://www.matmoz.si',
    'license': "AGPL-3",
    'contributors': [
        'Matjaž Mozetič <m.mozetic@matmoz.si>',
    ],
    "depends": [
        'l10n_base'
    ],
    "data": [
        'data_no/res.region.csv',
        'data_no/res.province.csv',
        'data_no/res.city.csv',
        'data_no/res.country.csv',
    ],
    "demo": [],
    "active": False,
    "installable": True
}
