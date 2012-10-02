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
    "depends": [
                "crm",
                "account",
                "analytic",
                "hr_timesheet_invoice",
                "project_time_schedule",
                "project_time_sequence",
                "project_time_milestone",
                "project_scope_wbs",
                "project_cost",
                "project_procurement",
                "project", 
                "project_issue",                    
                ],
    "description": """Extensions for the Project management module.     
    """,
    "init_xml": [
                ],
    "update_xml": [            
        "project_progress_report.xml",
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
