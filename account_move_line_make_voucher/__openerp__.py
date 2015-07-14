# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2014 Eficent (<http://www.eficent.com/>)
#              <contact@eficent.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

{
    "name": "Create Payment Vouchers from Journal Items",
    "version": "1.0",
    "author": "Eficent",
    "website": "www.eficent.com",
    "category": "Generic Modules/Payment",
    "depends": ["account", "account_voucher"],
    "description": """
Create Payment Vouchers from Journal Items
==========================================

    This module allows you to create Payment Vouchers from a list of Journal Items.
    The application creates as many Payment Vouchers as partners found in the selection.

    """,
    "init_xml": [],
    "update_xml": [
        "wizard/account_move_line_make_voucher_view.xml",
    ],
    'demo_xml': [

    ],
    'test': [],
    'installable': True,
    'active': False,
    'certificate': '',
}
