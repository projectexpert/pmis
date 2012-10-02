# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2011 Eficent (<http://www.eficent.com/>)
#              Jordi Ballester Alomar <jordi.ballester@eficent.com>
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
    "name": "Project Management",
    "version": "1.0",
    "author": "Jordi Ballester (Eficent)",
    "website": "http://www.eficent.com",
    "category": "Generic Modules/Projects & Services",
    "depends": ["account","product", "analytic", "board", "project","project_scope_wbs","project_cost"],
    "description": """Eficent Project Management. Project Cost Analysis
        - The aim is to enable the project manager can see at all times the relationshipbetween the planned cost, budget, 
        current theoretical cost actual cost of the project.
        - A report for analytic account Cost Analysis is provided. For each analytical account associated (taking into account the child accounts) breaks down the following information:
            * Analytical Account Code
            * Analytical Account Name
            * Planned Cost
            * Budgeted Cost
            * Current theoretical cost
            * Current Actual Cost
        - A report view to display the analytic resource usage. That is, comparing the planned and actual costs with the possibility to group by product, analytic account, period,... 
    """,
    "init_xml": [
                ],
    "update_xml": [        
        "security/ir.model.access.csv",               
        "account_analytic_balance_plan_report.xml",
        "wizard/account_analytic_balance_plan_report_view.xml",
        "report/account_analytic_resource_usage_view.xml",
        "report/account_analytic_resource_usage_product_view.xml",
        
    ],
    'demo_xml': [

    ],
    'test':[
    ],
    'installable': True,
    'active': False,
    'certificate': '',
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
