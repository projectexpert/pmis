# -*- encoding: utf-8 -*-
##############################################################################
#
# Copyright (c) 2013 Matmoz d.o.o. (info at matmoz.si)
#                          All Rights Reserved.
#
# WARNING: This program as such is intended to be used by professional
# programmers who take the whole responsability of assessing all potential
# consequences resulting from its eventual inadequacies and bugs
# End users who are looking for a ready-to-use solution with commercial
# garantees and support are strongly adviced to contract a Free Software
# Service Company
#
# This program is Free Software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#
##############################################################################

{
    'name': 'CRM cases part of Projects',
    'version': '0.7.3',
    'author': 'Matmoz d.o.o. (Didotech Group)',
    'website': 'http://www.matmoz.si',
    'category': 'Project Management',
    'description': """
    CRM tasks and CRM leads connected to project,
    crm cases tab on project view. In a project oriented
    company, every activity and comunication is part of a
    project thus all the leads and opportunities can be
    tracked also from the project form and since the issues
    are also a source of project communications, they're
    added as well in the view.
    """,
    'license': "AGPL-3",
    'contributors': [
        'Matjaž Mozetič <m.mozetic@matmoz.si>',
    ],
    'summary': '''CRM tasks and CRM leads connected to project''',
    'website':  'http://www.matmoz.si',
    'depends': ['crm_todo', 'project', 'project_issue'],
    'data': [
        'crm_todo_opportunity.xml',
        'crm_todo_project_task_tree.xml',
        'project_lead.xml',
        'project_opportunity.xml',
        'leads_project_view.xml'
    ],
    'qweb': [],
    'demo': [],
    'test': [],
    'active': False,
    'installable': True
}
