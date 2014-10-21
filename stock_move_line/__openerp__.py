# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2014 Eficent (<http://www.eficent.com/>)
#              Eficent <contact@eficent.com>
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
    "name": "Stock Move Line",
    "version": "1.0",
    "author": "Eficent",
    "website": "www.eficent.com",
    'summary': 'Creates move lines only for revenue and expenses',
    "depends": ["stock", "account_analytic_moves_extend"],
    "description": """
    - Limits the creation of analytic lines associated to stock moves to only occur when the move is associated to an expense or revenue account.
    - Introduces the  analytic account associated to tshe account move
    - Creates an analytic line associated to the expense or income account for that analytic account when the account move is created.    
    """,
    "init_xml": [],
    'data': [
             'stock_view.xml',
    ],
    'test':[
    ],
    'installable': True,
    'active': False,
    'certificate': '',
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
