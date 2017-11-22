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
    'name': 'Stock Analytic Account',
    'version': '8.0.1.0.1',
    'author':   'Eficent, '
                'Project Expert Team',
    'contributors': [
        'Jordi Ballester <jordi.ballester@eficent.com>',
    ],
    'website': 'http://project.expert',
    'category': 'Project Management',
    'license': 'AGPL-3',
    'depends': ['stock', 'analytic'],
    'data': [
             'view/stock_view.xml',
             'view/stock_picking_view.xml',
             'view/analytic_account_view.xml',
             # 'report/report_stock_analytic_account_view.xml',
             # 'report/report_stock_move_view.xml',
             'wizard/stock_change_product_qty_view.xml',
             'wizard/stock_fill_inventory_view.xml',
    ],
    'test': [
        'test/stock_users.yml',
        'demo/stock_demo.yml',
        'test/opening_stock.yml',
        'test/shipment.yml',
        'test/stock_report.yml',
        'test/setlast_tracking.yml',
    ],
    'installable': True,
    'active': False,
    'certificate': '',
}
