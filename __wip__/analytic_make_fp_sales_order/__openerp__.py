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
    "name": "Analytic - Create fixed price sales order",
    "version": "1.0",
    "author": "Eficent",
    "website": "www.eficent.com",
    "category": "Generic Modules/Projects & Services",
    "depends": ["sale","analytic", "analytic_plan", "sale_order_line_analytic"],
    "description": """
    """,
    "init_xml": [],
    "update_xml": [        
        "view/account_analytic_account_view.xml",
        "wizard/analytic_make_fp_sale_order.xml",
    ],
    'demo_xml': [

    ],
    'test':[
    ],
    'installable': True,
    'active': False,
    'certificate': '',
}