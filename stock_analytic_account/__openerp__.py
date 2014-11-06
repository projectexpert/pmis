# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2014 Eficent (<http://www.eficent.com/>)
#              Eficent <contact@eficent.com>
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
    "name": "Stock Analytic Account",
    "version": "1.0",
    "author": "Eficent",
    "website": "www.eficent.com",
    'summary': 'Adds the analytic account to stock moves',
    "depends": ["stock", "analytic"],
    "description": """
    - Adds the analytic account to the stock move
    - Makes it possible to search stock moves by analytic account or its project manager
    - Makes it possible to search picking lists by analytic account or its project manager
    """,
    "init_xml": [],
    'data': [
             'stock_view.xml',
             'stock_picking_view.xml',
    ],
    'test':[
    ],
    'installable': True,
    'active': False,
    'certificate': '',
}
