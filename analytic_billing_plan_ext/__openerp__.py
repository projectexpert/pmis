# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2014 Eficent (<http://www.eficent.com/>)
#               <contact@eficent.com>
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
    "name": "Analytic billing plan extension",
    "version": "1.0",
    "author": "Eficent",
    "website": "",
    "category": "Generic Modules/Projects & Services",
    "depends": ["analytic_billing_plan", "sale_order_line_analytic"],
    "description": """

  == Record planned sales and create sales orders  ==

    Variant to the Analytic Billing Plan module that works with module Sales order line analytic.
    That is, moves the analytic account to the sales order line.


   == More information and assistance ==

   If you are interested in this module and seek further assistance to use it please visit us at
   www.eficent.com or conact us at contact@eficent.com

    """,
    "init_xml": [],
    "update_xml": [],
    'demo_xml': [

    ],
    'test': [
    ],
    'installable': True,
    'active': False,
    'certificate': '',
}
