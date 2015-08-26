# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#    Copyright (C) 2014-Today Matmoz d.o.o. (<http://www.matmoz.si).
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
    'name': 'Tasks on CRM',
    'version': '1.0.3',
    'category': 'Project Management',
    'description': """
Todo list for CRM leads and opportunities.
==========================================
Based on the original crm_todo by Openerp SA, migrated from the version 7
to the version 8 by Matmoz d.o.o. and enhanced to interact with crm_project_task
for a better integration of CRM with project management.
    """,
    'license': "AGPL-3",
    'contributors': [
        'Matjaž Mozetič <m.mozetic@matmoz.si>',
    ],
    'summary': '''Todo list for CRM leads and opportunities''',
    'website':  'http://www.matmoz.si',
    'author':   'OpenERP SA, '
                'Matmoz d.o.o. (Didotech Group)',
    'website': 'http://www.matmoz.si',
    'depends': ['crm', 'project_gtd'],
    'data': ['crm_todo_view.xml'],
    'demo': ['crm_todo_demo.xml'],
    'installable': True,
    'auto_install': False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
