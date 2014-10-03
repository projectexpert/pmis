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
    "name": "Analytic Plan - Cost and revenue planning",
    "version": "1.0",
    "author": "Eficent",
    "website": "www.eficent.com",
    "category": "Generic Modules/Projects & Services",
    "depends": ["account", "analytic", "project"],
    "description": """
    == Manage analytic planned costs on your analytic accounts ==
    
    Eficent brings you this module to better manage the planne costs of your projects or cost centers.
  
    This module defines a new structure to record planning analytic lines of the analytic accounts.
    
    == New planning journal ==
    
    A planning journal is created. It is similar to the analytic journal, but used for planning purposes.
    
    The planning analytic journals can be configured.
    
    A planning analytic journal lines object is created, with the exceptions of referencing to the planning analytic journal instead of the analytic journal, and considering  that the general account is not a required entry.
  
    The new object is visible as a separate entity, accesible from the Accounting area, with the corresponding search, tree, form views.

    New analytic account planning attributes: cumulated planned costs, cummulated planned earnings and cumulated balance. The attributes are calculated based on the planning analytic journal lines.   

    The new attributes are visible on the following views: Analytic account forms: cumulated planned costs, cumulated planned earnings and cumulated balance; Budget positions: cumulated planned costs
    
    A report exists to create a PDF with the corresponding journal entries.

    == New planning versions ==
    You can define multiple planning versions for the analytic planning lines.


   == More information and assistance ==
   
   If you are interested in this module and seek further assistance to use it please visit us at www.eficent.com or conact us at contact@eficent.com

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