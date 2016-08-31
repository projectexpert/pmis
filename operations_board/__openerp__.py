# -*- encoding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2013 Matmoz d.o.o. (<http://www.matmoz.si>)
#
#
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
{
    'name': 'Operations Management Board',
    'version': '8.0.2.0.7',
    'category': 'Board/Projects & Services',
    'description': """
        Central operations menu that collects all the
        running tasks, issues, projects and leads/opportunities
        on the same place. A way to see what's going on in the
        company.

        The menu is placed under the messaging menu.
    """,
    'author': 'Matmoz d.o.o.',
    'website': 'http://www.matmoz.si',
    'license': 'AGPL-3',
    'depends': [
            'crm',
            'board',
            'mail',
            'project',
            'project_issue',
            'hr_timesheet',
            'analytic',
            'change_management',
            'web_dashboard_open_action'
    ],
    'data': ['board_ceo_view.xml'],
    'demo': [],
    'test': [],
    'qweb': [],
    'installable': True,
    'auto_install': False,
    'application': False,
}
