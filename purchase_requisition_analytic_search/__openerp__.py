# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2014 Eficent (<http://www.eficent.com/>)
#              <contact@eficent.com>
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
    "name": "Purchase Requisition Analytic Search",
    "version": "8.0.1.0.0",
    'author':   'Eficent, '
                'Project Expert Team',
    'contributors': [
        'Jordi Ballester <jordi.ballester@eficent.com>',
    ],
    'website': 'http://project.expert',
    'category': 'Project Management',
    'license': 'AGPL-3',
    "depends": [
        "analytic",
        "purchase_requisition",
        "purchase_requisition_line_analytic"
    ],
    "description": """
Organizations often require to integrate purchase requisitions with projects
or contracts,and to find requisitions by searching by it the project/contract
code, name or project/contract manager.
This module adds the following features to purchase requisitions:
* Adds the analytic account to the purchase requisition lines,
* When the purchase order is created from the purchase requisition, it copies
  the analytic account.
* Introduces the possibility to search purchase requisitions by analytic
  account or by project manager.
* Introduces a new menu entry in Purchasing to list purchase requisition lines.
""",
    "data": [
        "purchase_requisition_view.xml",
    ],
    'demo': [

    ],
    'test': [
    ],
    'installable': True,
    'active': False,
    'certificate': '',
}
