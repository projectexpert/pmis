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
from openerp.osv import fields, orm
from openerp.tools.translate import _


class AnalyticResourcePlanLine(orm.Model):

    _inherit = 'analytic.resource.plan.line'

    def _requested_qty(self, cr, uid, ids, name, arg, context=None):
        res = {}
        for line in self.browse(cr, uid, ids, context=context):
            requested_qty = 0.0
            for purchase_line in line.purchase_request_lines:
                requested_qty += purchase_line.product_qty
            res[line.id] = requested_qty
        return res

    _columns = {
        'requested_qty': fields.function(_requested_qty,
                                         string='Requested quantity',
                                         type='float',
                                         readonly=True),
        'purchase_request_lines': fields.many2many(
            'purchase.request.line',
            'purchase_request_line_analytic_resource_plan_line_line_rel',
            'analytic_resource_plan_line_id',
            'purchase_request_line_id',
            'Purchase Request Lines', readonly=True),
    }

    def unlink(self, cr, uid, ids, context=None):
        for line in self.browse(cr, uid, ids, context=context):
            if line.purchase_request_lines:
                raise orm.except_orm(
                    _('Error!'),
                    _('You cannot delete a record that refers to purchase '
                      'purchase request lines!'))
        return super(AnalyticResourcePlanLine, self).unlink(cr, uid, ids,
                                                            context=context)
