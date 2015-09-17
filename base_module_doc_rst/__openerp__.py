# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2009 Tiny SPRL (<http://tiny.be>).
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
    'name': 'Generate Docs of Modules',
    'version': '1.0',
    'category': 'Tools',
    'description': """
This module generates the Technical Guides of selected modules in Restructured Text format (RST).
=================================================================================================

Originally developed by OpenERP SA (version 6.1, http://www.odoo.com). This version was adapted
for the Odoo version 8 by Matmoz d.o.o. (http://www.matmoz.si).

    * It uses the Sphinx (http://sphinx.pocoo.org) implementation of RST
    * It creates a tarball (.tgz file suffix) containing an index file and one file per module
    * Generates Relationship Graph
    """,
    'author': 'OpenERP SA, Matmoz d.o.o.',
    'contributors': [
        'OpenERP SA',
        'Matjaž Mozetič <m.mozetic@matmoz.si>',
    ],
    'website': 'http://www.openerp.com',
    'depends': ['base'],
    'data': [
        'base_module_doc_rst_view.xml',
        'wizard/generate_relation_graph_view.xml',
        'wizard/tech_guide_rst_view.xml',
        'module_report.xml',
    ],
    'demo': [],
    'installable': True,
    'images': ['images/base_module_doc_rst1.jpeg'],
}
