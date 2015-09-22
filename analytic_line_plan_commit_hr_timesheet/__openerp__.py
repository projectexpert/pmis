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
    "name": "Project Cost committed costs on timesheets",
    "version": "1.1",
    "author": "Jordi Ballester (Eficent)",
    "website": "http://www.eficent.com",
    "category": "Generic Modules/Projects & Services",
    "depends": ["analytic_plan", "hr_timesheet"],
    "description": """
Eficent Project Management. Project Cost Planning Integration with HR
Timesheets:
   - When timesheets are recorded, the corresponding cost is registered as a
     commitment cost
    """,
    "data": [
        "hr_timesheet_view.xml",
    ],
    'demo': [

    ],
    'test': [
    ],
    'installable': True,
    'active': False,
    'certificate': '',
}
