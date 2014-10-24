# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2014 Eficent (<http://www.eficent.com/>)
#             <contact@eficent.com>
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
    "name": "Purchase Stock Analytic",
    "version": "1.0",
    "author": "Eficent",
    "website": "www.eficent.com",
    "category": "Purchase Orders, Receptions, Supplier Invoices",
    "depends": ["purchase", "stock_move_line"],
    "description": """
Copies the analytic account of the purchase order item to the stock move
    """,
    "init_xml": [],
    'data': [
    ],
    'test':[
    ],
    'installable': True,
    'active': False,
    'certificate': '',
}
