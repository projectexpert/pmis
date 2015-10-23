# -*- coding: utf-8 -*-
##############################################################################
#
#    Eficent
#    Copyright (C) 2014 (<http://www.eficent.com>).
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
    'name': 'Sale Stock Analytic',
    'version': '8.0.1.0.0',
    'summary': 'Copies the sales order analytic account to the stock move.',
    'author':   'Eficent, '
                'Project Expert Team',
    'contributors': [
        'Jordi Ballester <jordi.ballester@eficent.com>',
    ],
    'website': 'http://project.expert',
    'category': 'Project Management',
    'license': 'AGPL-3',
    'images': ['images/deliveries_to_invoice.jpeg'],
    'depends': [
        'sale_stock',
        'stock_move_line'
    ],
    'data': [],
    'demo': [],
    'test': [
             ],
    'installable': True,
    'auto_install': True,

}
