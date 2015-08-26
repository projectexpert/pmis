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
    'version': '0.1.2',
    'category': 'Project Management',
    'description': """This module allows linking of document pages to projects
        Based on the original project_wiki module from OpenERP 6.1 version
        by Agile Business Group""",
    'author':   'Agile Business Group,'
                'Matmoz d.o.o.',
    'website':  'http://www.agilebg.com ,'
                'http://www.matmoz.si',
    'license': 'AGPL-3',
    "depends": ['project', 'document_page'],
    "data": ['project_view.xml'],
    "qweb": [],
    "demo": [],
    "test": [],
    "active": False,
    "installable": True
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
