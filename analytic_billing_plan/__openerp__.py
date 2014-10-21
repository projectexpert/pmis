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
    "name": "Analytic billing plan",
    "version": "1.0",
    "author": "Eficent",
    "website": "",
    "category": "Generic Modules/Projects & Services",
    "depends": ["account", "sale", "analytic_plan"],
    "description": """
    
  == Record planned sales and create sales orders  ==
    
    Eficent brings you this module to automatically record the analytic planned sales associated to sales orders.
    
    You can create sales orders out of the planned sales.

            
   == More information and assistance ==
   
   If you are interested in this module and seek further assistance to use it please visit us at www.eficent.com or conact us at contact@eficent.com
        
    """,
    "init_xml": [],
    "update_xml": [
        "wizard/analytic_billing_plan_line_make_sale.xml",
        "analytic_billing_plan_view.xml",
        "analytic_account_view.xml",
        "product_view.xml",
        "project_view.xml",
        "security/ir.model.access.csv",
        
    ],
    'demo_xml': [

    ],
    'test':[
    ],
    'installable': True,
    'active': False,
    'certificate': '',
}
