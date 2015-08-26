# -*- encoding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2014 Didotech Srl - OpenERP 7 migration by Matmoz d.o.o.
#    $Id$
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
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
    'author': 'Didotech@Matmoz',
    'website': 'http://www.didotech.com',
    'license': 'AGPL-3',
    "depends": [
        'l10n_base'
    ],
    "init_xml": [],
    "update_xml": [
        'data_no/res.region.csv',
        'data_no/res.province.csv',
        'data_no/res.city.csv',
        'data_no/res.country.csv',
    ],
    "demo_xml": [],
    "active": False,
    "installable": True
}

# http://www.istat.it/strumenti/definizioni/comuni/
# i dati dovrebbero essere sincronizzati con questi
