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
    "name": "Analytic Plan",
    "version": "1.0",
    "author": "Eficent",
    "website": "www.eficent.com",
    "category": "Generic Modules/Projects & Services",
    "depends": ["account", "analytic", "project", "project_wbs"],
    "description": """
Analytic Plan
====================================
    An effective planning of costs and revenues associated to projects or to other analytic accounts
    becomes essential in organizations that are run by projects, or profit center accounting.
    The process of cost planning generally follows an rolling wave planning approach, in which
    the level of detail of the planned costs is increases over time, as the details of the work required
    are known to the planning group.

    The module 'Analytic Plan' provides the foundation for the planning of analytic costs and revenues, and it is
    used by other modules that can originate planned costs or revenues during the business process
    execution.

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


Define Analytic Planning Lines:
------------------------------------
    The analytic planning lines are used to capture the planned cost or revenue, for a given planning version.
    They are equivalent to the analytic lines, used to capture the actual cost or revenue.

Changes to the Analytic Account:
------------------------------------------------------------------
    The analytic account incorporates new analytic account planning attributes:
        * Cumulated planned costs. Adds up all the planned costs of this analytic account as well as the child analytic accounts.
        * Cumulated planned revenues. Adds up all the planned revenues of this analytic account as well as the child analytic accounts.
        * Cumulated balance. Provides the difference between cumulated costs and revenues.

    The attributes are calculated, for an analytic account, based on the planning analytic journal lines
       and based on the active planning version defined on that analytic account.

    Users with permissions to access to analytic accounts can navigate from the analytic account to the
     to the associated Analytic Planning Lines.

More information and assistance:
-----------------------------------
    If you are interested in this module and seek further assistance to use it please visit
    us at www.eficent.com or conact us at contact@eficent.com.

    """,
    "init_xml": [],
    "update_xml": [
        "account_analytic_plan_version_view.xml",
        "account_analytic_plan_version_data.xml",
        "account_analytic_plan_journal_view.xml",
        "account_analytic_line_plan_view.xml",
        "account_analytic_account_view.xml",
        "security/ir.model.access.csv",
        "security/project_cost_security.xml",
        "account_analytic_plan_journal_data.xml",
        "project_view.xml",  
    ],
    'demo_xml': [

    ],
    'test':[
    ],
    'installable': True,
    'active': False,
    'certificate': '',
}