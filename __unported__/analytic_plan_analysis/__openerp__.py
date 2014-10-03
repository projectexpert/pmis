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
    "name": "Project Cost Analysis",
    "version": "1.0",
    "author": "Eficent",
    "website": "www.eficent.com",
    "category": "Generic Modules/Projects & Services",
    "depends": ["account", "product", "analytic", "project","project_wbs","analytic_plan"],
    "description": """
    
    == Analyze the costs of your project ==
    Eficent brings you this module to better analyze the costs of your projects.
    
    The aim is to enable the project manager can see at all times the relationship between the planned cost, budget, current theoretical cost actual cost of the project.
    
    The following reports are defined:
    
    Resource usage analysis: For each analytical account associated (taking into account the child accounts) breaks down the following information: Analytical Account Code, Analytical Account Name, Planned Cost, Budgeted cost, Commited cost, Current Actual Cost            
    Resource usage (amounts): Provides a chart view of the resource usage per analytic account, based on amounts.
    Resource usage (quantities): Provides a chart view of the resource usage per analytic account, based on quantities.

    Resource usage analysis by product: For each analytical account and product associated (taking into account the child accounts) breaks down the following information: Analytical Account Code, Analytical Account Name, Planned Cost, Budgeted cost, Commited cost, Current Actual Cost  
    Resource usage by product (amounts): Provides a chart view of the resource usage per analytic account and product, based on amounts.
    Resource usage by product (quantities): Provides a chart view of the resource usage per analytic account and product, based on quantities.
 
    The following PDF forms are defined:
    
    Analytic Planning Balance: Provides the total credit, debit, balance and quantiy for the planned and actual costs and revenues. 
    
    
    """,
    "init_xml": [
                ],
    "update_xml": [        
        "security/ir.model.access.csv",               
        "account_analytic_balance_plan_report.xml",
        "wizard/account_analytic_balance_plan_report_view.xml",
        "report/account_analytic_resource_usage_view.xml",
        "report/account_analytic_resource_usage_product_view.xml",
        "report/account_analytic_plan_actual_view.xml",
        
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
