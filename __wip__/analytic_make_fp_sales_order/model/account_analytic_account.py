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
import decimal_precision as dp
from osv import fields, osv


class account_analytic_account(osv.osv):
    
    _inherit = 'account.analytic.account'

    _columns = {
        'sale_gross_margin': fields.float('% Gross Margin',
                                          help='Planned % Gross Margin, '
                                               'in fixed price contracts. '
                                               'It is considered when creating a '
                                               'sales order from the Analytic Account.',
                                          digits_compute=dp.get_precision('Account')),
        'sale_product_uom_id': fields.many2one('product.uom', 'UoM'),
        'sale_qty': fields.float('Quantity',
                                 digits_compute=dp.get_precision('Account')),
        'sale_product_id': fields.many2one('product.product', 'Product'),
        'sale_name': fields.char('Description'),
        'sale_notes': fields.text('Notes'),
    }


account_analytic_account()