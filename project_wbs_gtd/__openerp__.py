# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
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
    'name': 'Project Level Todo',
    'version': '8.0.1.0.3',
    'author': 'OpenERP SA, '
              'Matmoz d.o.o., '
              'Project Expert Team',
    'contributors': [
        'Matjaž Mozetič <m.mozetic@matmoz.si>',
    ],
    'website': 'http://project.expert',
    'category': 'Project Management',
    'license': 'AGPL-3',
    'summary': '''GTD View on Project WBS Level''',
    'depends': ['project', 'project_gtd'],
    'data': [
        'project_gtd_data.xml',
        'project_gtd_view.xml',
        'security/ir.model.access.csv',
        'wizard/project_gtd_empty_view.xml',
        'wizard/project_gtd_fill_view.xml',
    ],
    'demo': ['project_gtd_demo.xml'],
    'test': ['test/wbs_timebox.yml'],
    'installable': True,
    'auto_install': False,
}
