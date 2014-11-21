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
from tools.translate import _
from osv import fields, osv


class sale_order_line_billing_milestone(osv.osv):

    _name = 'sale.order.line.billing.milestone'
    _description = "Sale Order Line Billing Milestone "

    _columns = {
        'order_id': fields.related('order_line_id', 'order_id', type='many2one',
                                   relation='sale.order', string='Sales Order'),
        'order_line_id': fields.many2one('sale.order.line', 'Sales Order Line',
                                         required=True, ondelete='cascade', select=True),
        'name': fields.char('Name', required=True),
        'date': fields.date('Milestone billing date', required=True),
        'percent': fields.float('% to bill'),
        'amount': fields.float('Fixed amount  to bill',
                               digits_compute=dp.get_precision('Sale Price')),
        'state': fields.selection([('blocked', 'Blocked for Billing'),
                                   ('released', 'Released for Billing'),
                                   ('billed', 'Billed')],
                                  'Status', select=True, required=True),
        'task_id': fields.many2one('project.task', 'Project Task')
    }

    _defaults = {
        'state': 'blocked',
    }
sale_order_line_billing_milestone()