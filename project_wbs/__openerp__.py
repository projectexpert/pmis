# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2014 Eficent (<http://www.eficent.com/>)
#             <contact@eficent.com>
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
    "name": "Work Breakdown Structure",
    "version": "2.0",
    "author": "Eficent",
    "website": "www.eficent.com",
    "category": "Generic Modules/Projects & Services",
    "depends": ["project","analytic"],
    "description": """Project Scope  
    - The hierarchy of a project is considered the WBS (Work Breakdown Structure)
    - The analytic accounts in the project hierarchies are considered WBS components 
    - The analytic account code is shown in the project
    - The complete WBS path code  is shown in the analytic account and in the project
    - The complete WBS path name is shown in the analytic account and in the project
    - The WBS paths are concatenated with /
    - It is possible to search projects by complete WBS path code & name
    - It is possible to search tasks by project complete WBS path code & name
    - The WBS components can be classified as project, phase, deliverable, work package. 
    - The classification is shown in the project and analytic account views
    - A project stage attribute is incorporated in the analytic account and displayed in the project and analytic account views.
     
    """,
    "init_xml": [],
    "update_xml": [
        "analytic_account_stage_view.xml",
        "account_analytic_account_view.xml",
        "project_project_view.xml",
        "project_task_view.xml",
        "security/ir.model.access.csv",
    ],
    'demo_xml': [

    ],
    'test':[
    ],
    'installable': True,
    'active': False,
    'certificate': '',
    'application': True,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
