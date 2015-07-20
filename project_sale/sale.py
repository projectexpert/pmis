# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
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


class sale_order(osv.osv):

    _inherit = "sale.order"

    _columns = {
        'project': fields.many2one(
            'project.project',
            'Project',
            readonly=True,
            states={'draft': [('readonly', False)]},
            help="The project related to a sales order."
        ),
        'project_manager': fields.related(
            'project',
            'user_id',
            readonly=True,
            string='Project Manager',
            type='many2one',
            relation="res.users",
            store=True
        ),
    }

sale_order()


class sale_order_line(osv.osv):

    _inherit = 'sale.order.line'

    _columns = {
        'order_project': fields.related(
            'order_id', 'project', type='many2one', relation='project.project', store=True, string='Project'
        ),
        'order_project_manager': fields.related(
            'order_project', 'user_id', readonly=True, string='Project Manager', type='many2one',
            relation="res.users", store=True
        ),
    }

    def _prepare_order_line_invoice_line(self, cr, uid, line, account_id=False, context=None):
        res = super(sale_order_line, self)._prepare_order_line_invoice_line(cr, uid, line, account_id, context)
        res['account_analytic_id'] = line.order_id.project and line.order_id.project.analytic_account_id \
            and line.order_id.project.analytic_account_id.id or res['account_analytic_id']
        return res


class project(osv.osv):
    _inherit = "project.project"

    def _get_sale_project_id(self, cr, uid, ids, context=None):
        project_id = []
        for sale_order_obj in self.pool.get('sale.order').browse(cr, uid, ids, context=context):
            project_id.append(sale_order_obj.project.id)
        return project_id

    def _order_count(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        for id in ids:
            order_ids = self.pool.get('sale.order').search(cr, uid, [('project.id', '=', id)], context=context)
            order_count = order_ids and len(order_ids) or 0
            res[id] = order_count
        return res

    _columns = {
                'order_count': fields.function(
                    _order_count, method=True, type='integer', string='Associated Sale Order(s)',
                    # store={
                    # 'sale.order' : (_get_sale_project_id, ['project'],5),
                    # }, help="Gives the number of sale order associated with the project"
                ),
                }

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
