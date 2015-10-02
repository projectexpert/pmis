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
from openerp.tools.translate import _
from openerp.osv import fields, orm
# from openerp import netsvc
import openerp.addons.decimal_precision as dp


class AnalyticResourcePlanLineMakePurchaseRequest(orm.TransientModel):
    _name = "analytic.resource.plan.line.make.purchase.request"
    _description = "Resource plan make purchase request"

    _columns = {
        'origin': fields.char('Origin', size=32, required=True),
        'description': fields.text('Description'),
        'item_ids': fields.one2many(
            'analytic.resource.plan.line.make.purchase.request.item',
            'wiz_id', 'Items'),
    }

    def _prepare_item(self, cr, uid, line, context=None):
        return [{
            'account_id': line.account_id.id,
            'product_id': line.product_id.id,
            'product_qty': line.unit_amount,
            'product_uom_id': line.product_uom_id.id,
            'line_id': line.id,
        }]

    def default_get(self, cr, uid, fields, context=None):
        res = super(AnalyticResourcePlanLineMakePurchaseRequest,
                    self).default_get(cr, uid, fields, context=context)
        res_plan_obj = self.pool['analytic.resource.plan.line']
        resource_plan_line_ids = context.get('active_ids', [])
        active_model = context.get('active_model')

        if not resource_plan_line_ids:
            return res
        assert active_model == 'analytic.resource.plan.line', \
            'Bad context propagation'

        items = []
        for line in res_plan_obj.browse(cr, uid, resource_plan_line_ids,
                                        context=context):
                items += self._prepare_item(cr, uid, line, context=context)
        res['item_ids'] = items
        return res

    def _prepare_purchase_request(self, cr, uid, make_purchase_request,
                                  company_id, context=None):
        data = {
            'company_id': company_id,
            'origin': make_purchase_request.origin,
            'description': make_purchase_request.description,
            }
        return data

    def _prepare_purchase_request_line(self, cr, uid, pr_id,
                                       make_purchase_request, item,
                                       context=None):
        return {
            'request_id': pr_id,
            'name': item.product_id.name,
            'product_qty': item.product_qty,
            'product_id': item.product_id.id,
            'product_uom_id': item.product_uom_id.id,
            'date_required': item.line_id.date or False,
            'analytic_account_id': item.line_id.account_id.id,
            'analytic_resource_plan_lines': [(4, item.line_id.id)]
        }

    def make_purchase_request(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        res = []
        make_purchase_request = self.browse(cr, uid, ids[0], context=context)
        line_plan_obj = self.pool['analytic.resource.plan.line']
        request_obj = self.pool['purchase.request']
        request_line_obj = self.pool['purchase.request.line']
        company_id = False
        warehouse_id = False
        request_id = False
        for item in make_purchase_request.item_ids:
            line = item.line_id
            if line.state != 'confirm':
                raise orm.except_orm(
                    _('Could not create purchase request !'),
                    _('All resource plan lines must be  '
                      'confirmed.'))
            if item.product_qty < 0.0:
                raise orm.except_orm(
                    _('Could not create purchase request !'),
                    _('Enter a positive quantity.'))

            line_company_id = line.account_id.company_id \
                and line.account_id.company_id.id or False
            if company_id is not False \
                    and line_company_id != company_id:
                raise orm.except_orm(
                    _('Could not create purchase request !'),
                    _('You have to select lines '
                      'from the same company.'))
            else:
                company_id = line_company_id

            line_warehouse_id = line.account_id.warehouse_id \
                and line.account_id.warehouse_id.id or False
            if warehouse_id is not False \
                    and line_warehouse_id != warehouse_id:
                raise orm.except_orm(
                    _('Could not create purchase request !'),
                    _('You have to select lines '
                      'from the same warehouse.'))
            else:
                warehouse_id = line_warehouse_id

            if request_id is False:
                request_data = self._prepare_purchase_request(
                    cr, uid, make_purchase_request, company_id,
                    context=context)
                request_id = request_obj.create(cr, uid, request_data,
                                                context=context)
            request_line_data = self._prepare_purchase_request_line(
                cr, uid, request_id, make_purchase_request, item,
                context=context)
            request_line_id = request_line_obj.create(
                cr, uid, request_line_data, context=context)
            values = {
                'purchase_request_lines': [(4, request_line_id)]
            }
            line_plan_obj.write(cr, uid, [line.id],
                                values, context=context)
            project_manager_id = line.account_id.user_id and \
                line.account_id.user_id.partner_id.id or False
            if project_manager_id:
                request = request_obj.browse(cr, uid, request_id,
                                             context=context)
                message_follower_ids = [x.id for x in
                                        request.message_follower_ids]
                if project_manager_id not in message_follower_ids:
                    request_obj.write(cr, uid, request_id, {
                        'message_follower_ids': (4, project_manager_id)})
            res.append(request_line_id)

        return {
            'domain': "[('id','in', ["+','.join(map(str, res))+"])]",
            'name': _('Purchase Request Lines'),
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'purchase.request.line',
            'view_id': False,
            'context': False,
            'type': 'ir.actions.act_window'
        }


class AnalyticResourcePlanLineMakePurchaseRequestItem(orm.TransientModel):
    _name = "analytic.resource.plan.line.make.purchase.request.item"
    _description = "Resource plan make purchase request item"

    _columns = {
        'wiz_id': fields.many2one(
            'analytic.resource.plan.line.make.purchase.request',
            'Wizard', required=True, ondelete='cascade',
            readonly=True),
        'line_id': fields.many2one('analytic.resource.plan.line',
                                   'Resource Plan Line',
                                   required=True,
                                   readonly=True),
        'account_id': fields.related('line_id',
                                     'account_id', type='many2one',
                                     relation='account.analytic.account',
                                     string='Analytic Account',
                                     readonly=True),
        'product_id': fields.related('line_id',
                                     'product_id', type='many2one',
                                     relation='product.product',
                                     string='Product',
                                     readonly=True),
        'product_qty': fields.float(string='Quantity to request',
                                    digits_compute=dp.get_precision(
                                        'Product UoS')),
        'product_uom_id': fields.related('line_id',
                                         'product_uom_id', type='many2one',
                                         relation='product.uom',
                                         string='UoM',
                                         readonly=True)
    }
