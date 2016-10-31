# -*- encoding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2014 Didotech Srl - Odoo 7 and 8 migration by Matmoz d.o.o.
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
    'name': 'Base Localization',
    'version': '8.0.4.0.1',
    'category': 'Localization',
    'summary': "Base Localization Module for sub-regions",
    'author':   'Didotech, '
                'Matmoz d.o.o.',
    'website': 'http://www.matmoz.si',
    'license': "AGPL-3",
    'contributors': [
        'Matjaž Mozetič <m.mozetic@matmoz.si>',
        'Andrei Levin <andrei.levin@didotech.com'
        ],
    "depends": [
        'base'
    ],
    "data": [
        'partner/partner_view.xml',
        "security/ir.model.access.csv",
        'data/res.country.csv',
    ],
    "qweb": [],
    "demo": [],
    "test": [],
    "active": False,
    "installable": True
}
