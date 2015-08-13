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
import openerp.addons.decimal_precision as dp
from openerp.osv import fields, osv


class analytic_resource_plan_line(osv.osv):

    _inherit = 'analytic.resource.plan.line'

    def _has_active_order(self, cr, uid, ids, fields, arg, context=None):
        res = {}
        if context is None:
            context = {}

        for plan_line in self.browse(cr, uid, ids, context=context):
            res[plan_line.id] = False
            for order_line in plan_line.order_line_ids:
                if order_line.state and order_line.state != 'cancel':
                    res[plan_line.id] = True
        return res

    _columns = {
        'order_line_ids': fields.many2many(
            'purchase.order.line',
            'analytic_resource_plan_order_line_rel',
            'order_line_id',
            'analytic_resource_plan_line_id'
        ),

        'has_active_order': fields.function(
            _has_active_order,
            method=True,
            type='boolean',
            string='Order',
            help='''
            Indicates that this resource plan line
            contains at least one non-cancelled purchase order.
            '''
        ),
    }

    def copy(self, cr, uid, id, default=None, context=None):
        if context is None:
            context = {}
        if default is None:
            default = {}
        default['order_line_ids'] = []
        res = super(analytic_resource_plan_line, self).copy(
            cr, uid, id, default, context)
        return res

analytic_resource_plan_line()
