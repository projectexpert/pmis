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


_REQUEST_STATE = [
    ('none', 'No Request'),
    ('draft', 'Draft'),
    ('to_approve', 'To be approved'),
    ('approved', 'Approved'),
    ('rejected', 'Rejected')
]


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

    def _get_request_state(self, cr, uid, ids, names, arg, context=None):
            res = {}
            for line in self.browse(cr, uid, ids, context=context):
                res[line.id] = 'none'
                if any([pr_line.request_id.state == 'approved' for pr_line in
                        line.purchase_request_lines]):
                    res[line.id] = 'approved'
                elif all([pr_line.request_id.state == 'cancel' for pr_line in
                          line.purchase_request_lines]):
                    res[line.id] = 'cancel'
                elif all([po_line.request_id.state in ('to_approve', 'cancel')
                          for po_line in line.purchase_request_lines]):
                    res[line.id] = 'to_approve'
                elif any([po_line.request_id.state == 'approved' for po_line in
                          line.purchase_request_lines]):
                    res[line.id] = 'approved'
                elif all([po_line.request_id.state in ('draft', 'cancel')
                          for po_line in line.purchase_request_lines]):
                    res[line.id] = 'draft'
            return res

    def _get_rpls_from_purchase_requests(self, cr, uid, ids, context=None):
        rpl_ids = []
        for request in self.pool['purchase.request'].browse(
                cr, uid, ids, context=context):
            for request_line in request.line_ids:
                for rpl in request_line.analytic_resource_plan_lines:
                    rpl_ids.append(rpl.id)
        return list(set(rpl_ids))

    def _get_rpls_from_purchase_request_lines(self, cr, uid, ids,
                                              context=None):
        rpl_ids = []
        for request_line in self.pool['purchase.request.line'].browse(
                cr, uid, ids, context=context):
            for rpl in request_line.analytic_resource_plan_lines:
                rpl_ids.append(rpl.id)
        return list(set(rpl_ids))

    _columns = {
        'requested_qty': fields.function(_requested_qty,
                                         string='Requested quantity',
                                         type='float',
                                         readonly=True),
        'request_state': fields.function(
            _get_request_state, string='Request status', type='selection',
            selection=_REQUEST_STATE,
            store={'purchase.request':
                   (_get_rpls_from_purchase_requests,
                    ['state', 'line_ids'], 10),
                   'purchase.request.line':
                   (_get_rpls_from_purchase_request_lines,
                    ['analytic_resource_plan_lines'], 10)}),
        'purchase_request_lines': fields.many2many(
            'purchase.request.line',
            'purchase_request_line_analytic_resource_plan_line_line_rel',
            'analytic_resource_plan_line_id',
            'purchase_request_line_id',
            'Purchase Request Lines', readonly=True),
    }

    _defaults = {
        'request_state': 'none',
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
