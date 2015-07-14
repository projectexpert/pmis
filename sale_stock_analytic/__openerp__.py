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
    'version': '1.0',
    'category': 'Hidden',
    'summary': 'Copies the analytic account of the sales order to the stock move.',
    'description': """
Copies the analytic account of the sales order to the stock move.
""",
    'author': 'Eficent',
    'website': 'http://www.eficent.com',
    'images': ['images/deliveries_to_invoice.jpeg'],
    'depends': [
        'sale_stock',
        'stock_move_line'
    ],
    "data": [],
    'demo': [],
    'test': [
             ],
    'installable': True,
    'auto_install': True,

}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
