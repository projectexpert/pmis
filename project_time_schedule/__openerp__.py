# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2011 Eficent (<http://www.eficent.com/>)
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
    "name": "Project Time Management - Activity Scheduling",
    "version": "1.0",
    "author": "Eficent",
    "website": "http://www.eficent.com",
    "category": "Generic Modules/Projects & Services",
    "depends": ["project"],
    "description": """
        - The user accesses from Project - Project – Tasks to the list of tasks and milestones.
        A new tab "Scheduling" appears under Other Info.
        This tab displays attributes relating to the task scheduling.
        - The network diagram is first determined, based on the relationships between activities.
        - Starting from the first activity identified, the network goes forward first to determine the early dates
        of tasks, taking into account the task durations, limitations imposed start date of tasks or actual start date.
        - Starting from the last activity identified, the network is executed
        backwards to determine the late date, taking into account the task
        durations, limitations to date of completion of the work or the actual end dates.
        - For those tasks that are in the critical path of the network indicator is marked "Is in the Critical Path
        - The Total Margin (Total float) and Free margin (Free Float) is determined.
        - The method used is the Critical Chain Method (http://en.wikipedia.org/wiki/Critical_Path_Method).
        - The method is calculated taking into account an existing algorithm, similar to the following existing code:
        (http://www.codeproject.com/KB/recipes/CriticalPathMethod.aspx).
        - The critical path is calculated using the Dijkstra algorithm


    """,
    "data": [
        "project_time_schedule_view.xml",
    ],
    'demo': [

    ],
    'test': [
    ],
    'installable': True,
    'active': False,
    'certificate': '',
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
