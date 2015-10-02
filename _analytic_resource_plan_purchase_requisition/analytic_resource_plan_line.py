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
from openerp.osv import fields, osv


class analytic_resource_plan_line(osv.osv):

    _inherit = 'analytic.resource.plan.line'

    def _has_active_requisition(self, cr, uid, ids, fields, arg, context=None):
        res = {}
        if context is None:
            context = {}

        for plan_line in self.browse(cr, uid, ids, context=context):
            res[plan_line.id] = False
            for requisition_line in plan_line.requisition_line_ids:
                if (
                    requisition_line.requisition_id and
                    requisition_line.requisition_id.state and
                    requisition_line.requisition_id.state != 'cancel'
                ):
                    res[plan_line.id] = True

        return res

    _columns = {
        'requisition_line_ids': fields.many2many(
            'purchase.requisition.line',
            'analytic_resource_plan_line_requisition_line_rel',
            'requisition_line_id',
            'resource_plan_line_id'
        ),

        'has_active_requisition': fields.function(
            _has_active_requisition,
            method=True,
            type='boolean',
            string='Requisition',
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
        default['requisition_line_ids'] = []
        res = super(analytic_resource_plan_line, self).copy(
            cr, uid, id, default, context)
        return res

analytic_resource_plan_line()
