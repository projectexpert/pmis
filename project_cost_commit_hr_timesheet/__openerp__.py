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
    "depends": ["project_cost","hr_timesheet"],
    "description": """Eficent Project Management. Project Cost Planning Integration with HR Timesheets
        - When timesheets are recorded, the corresponding cost is registered as a commitment cost
    """,
    "init_xml": [],
    "update_xml": [                                      
        "hr_timesheet_view.xml", 
        "hr_timesheet_data.xml", 
        "hr_timesheet_workflow.xml",         
        "account_analytic_line_commit_view.xml",
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
