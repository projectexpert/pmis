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
    "name": "Analytic Resource Planning - Purchase Requisitions",
    "version": "1.1",
    "author": "Eficent",
    "website": "www.eficent.com",
    "category": "Generic Modules/Projects & Services",
    "depends": [
        "analytic_resource_plan",
        "purchase_requisition",
        "purchase_requisition_line_analytic",
        "purchase_requisition_line_description",
    ],
    "description": """
THIS MODULE IS GOING TO BE DEPRECATED, USE
analytic_resource_plan_purchase_request INSTEAD

== Record  planned costs and create purchase requisitions  ==

Eficent brings you this module to create purchase requisitions from analytic
planning lines. This module depends on modules provided by Vauxoo, that can
be obtained from Odoo Apps:
    - purchase_requisition_line_analytic
    - purchase_requisition_line_description

== More information and assistance ==

If you are interested in this module and seek further assistance to use it
please visit us at www.eficent.com or conact us at contact@eficent.com


    """,
    "data": [
        "wizard/analytic_resource_plan_line_make_purchase_requisition.xml",
        "analytic_resource_plan_line_view.xml",
        "analytic_account_view.xml",

    ],
    'demo': [

    ],
    'test': [
    ],
    'installable': False,
    'active': False,
    'certificate': '',
}
