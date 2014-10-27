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
    "name": "Work In Progress Statement",
    "version": "1.0",
    "author": "Eficent",
    "website": "",
    "category": "Generic Modules/Projects & Services",
    "depends": [
                "analytic",
                "analytic_plan",
                "project_wbs",
                ],
    "description": """
Work In Progress Statement
====================================

    The Revenue Principle of GAAP requires Revenue to be recorded in the period it is Earned
    regardless of when it is billed or when cash is received.

    In some cases, it is simple to determine the timing for Revenues Earned, once ownership of
    a product is transferred or a service is complete, revenue is considered to have been earned.

    But if revenue recognition were delayed until the end of a long term contract,
    the Matching Principle of tying revenues and their direct costs to each other would be violated.
    The solution to this problem is the Percentage of Completion method of Revenue Recognition.

    Contract Revenues are tied to Costs, but Billings on Contracts are not always tied to Costs.
    Sometimes elements of a contract are billed in advance or sometimes they are delayed by mutual agreement
    (or disagreement).

    This mismatch between actual billed revenue and earned revenue will require an adjusting entry but
    since the Percentage of Completion method adjusts billed revenue to reflect earned revenue,
    billings are posted to revenues and adjusted later to reflect the correct earned revenue amount.
    (Debit Accounts Receivable, Credit Sales).

    Long Term Contracts will have estimates for both sides of a contract, Costs and Revenues.
    Calculating Percentage of Completion requires both total actual and total estimated numbers to
    calculate a percentage so it uses the side where both the actual and estimated numbers can be known, Costs.

    Percent Complete = Actual Costs to Date / Total Estimated Costs
    The Percent Complete is then applied to the Total Estimated Revenue to determine Earned Revenue to Date.

    Earned Revenue to Date = Percent Complete * Total Estimated Revenue
    Finally, the Earned Revenue to Date is compared to the Billings on Contract to Date.
    The difference is either added to or subtracted from the Revenue.

    Total Billings on Contract - Earned Revenue to Date = Over/Under Billed Revenue

    The Over/Under Billed Revenue accounts are Balance Sheet Accounts and they are often called either
    Billings in Excess of Costs (liability account that reflects over-billings)
    or Costs in Excess of Billings (asset account that reflects under-billings).

Work in Progress Statement
-----------------------------------------------
    The Work In Progress Statement is associated to the Percentage of Completion Method, and is
    used to compile the information necessary for the percentage of completion calculations, but also to
    provide crucial information about the total value and progress of work on hand inventory.

    Source: http://www.accountingunplugged.com/2008/09/11/percentage-of-completion-work-in-progress/

    The statement provides the following information
        * Contract/Project name.
        * Contract/Project code.
        * Contract/Project Value. As the Total Estimated Revenue of the contract.
        * Actual Billings to Date. Total invoiced amount issued to the customer to date.
        * Actual Costs to Date.
        * Total Estimated Costs.
        * Estimated Costs to Complete. Total Estimated Costs – Actual Costs to Date.
        * Estimated Gross Profit. Contract Value – Total Estimated Costs.
        * Percent Complete. Actual Costs to Date / Total Estimated Costs.
        * Earned Revenue to Date. Percent Complete * Total Estimated Revenue
        * Over Billings. Total Billings on Contract – Earned Revenue to Date (when > 0 )
        * Under Billings. Total Billings on Contract – Earned Revenue to Date (when < 0 )

More information and assistance:
-----------------------------------
    If you are interested in this module and seek further assistance to use it please visit
    us at www.eficent.com or conact us at contact@eficent.com.

    """,

    "init_xml": [
                ],
    "update_xml": [            
        "analytic_wip_report.xml",
        "security/ir.model.access.csv",
        "account_analytic_account_view.xml",
    ],
    'demo_xml': [

    ],
    'test':[
    ],
    'installable': True,
    'active': False,
    'certificate': '',
}