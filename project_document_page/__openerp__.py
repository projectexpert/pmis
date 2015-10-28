# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2010 (Original Author)
#    Domsense s.r.l. (<http://www.domsense.com>)
#    Copyright (C) 2014 (OpenERP version 7&8 adaptation)
#    Matmoz d.o.o. (<http://www.matmoz.si>)
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
    'name': 'Document pages for project',
    'version': '8.0.1.0.2',
    'author':   'Agile Business Group, '
                'Matmoz d.o.o., '
                'Project Expert Team',
    'contributors': [
        'Lorenzo Battistini <lorenzo.battistini@domsense.com>',
        'Matjaž Mozetič <m.mozetic@matmoz.si>',
    ],
    'website': 'http://project.expert',
    'category': 'Project Management',
    'license': 'AGPL-3',
    "depends": ['project', 'document_page'],
    "data": ['project_view.xml'],
    "qweb": [],
    "demo": [],
    "test": [],
    "active": False,
    "installable": True
}
