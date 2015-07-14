# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2014 Eficent (<http://www.eficent.com/>)
#              Jordi Ballester Alomar <jordi.ballester@eficent.com>
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
    'summary': 'Adds the analytic account to stock moves.',
    "depends": ["stock", "analytic", "stock_analytic_account"],
    "description": """
    - Limits the creation of analytic lines associated to stock moves to only occur when the move is associated
      to an expense or revenue account.
    """,
    'data': [
    ],
    'test': [
    ],
    'installable': True,
    'active': False,
    'certificate': '',
}
