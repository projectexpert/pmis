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
    "name": "Analytic Resource Planning - Purchase Orders",
    "version": "1.0",
    "author": "Eficent",
    "website": "www.eficent.com",
    "category": "Generic Modules/Projects & Services",
    "depends": ["purchase", "analytic_resource_plan"],
    "description": """
Resource Plan
====================================
    An effective planning of costs and revenues associated to projects or to other analytic accounts
    becomes essential in organizations that are run by projects, or profit center accounting.
    The process of cost planning generally follows an rolling wave planning approach, in which
    the level of detail of the planned costs is increases over time, as the details of the work required
    are known to the planning group.

    The module 'Resource Plan' makes it possible to plan the resources required for a project and determines
    the cost associated with them. It provides also the possibility to create purchase orders f

Define Planning Versions:
------------------------------------
    Organizations typically maintain different versions of their planned costs (rough cut, detailed,
    approved budget, committed,...).
    A Planning Version is defined by the following attributes:
        * Name
        * Code
        * Active: The planning version is active for use in the cost planning
        * Default version for committed costs: This planning version should be used for committed costs
        * Default planning version: This version is proposed by default

Define Analytic Planning Journals:
------------------------------------
    The Analytic Planning Journal serves as an attribute to classify the costs or revenue by the it's origin.
    It is equivalent to the Analytic Journal.

    """,
    "init_xml": [],
    "update_xml": [        
        "wizard/analytic_resource_plan_line_make_purchase.xml",
        "analytic_resource_plan_line_view.xml",
        "analytic_account_view.xml",
        
    ],
    'demo_xml': [

    ],
    'test':[
    ],
    'installable': True,
    'active': False,
    'certificate': '',
}