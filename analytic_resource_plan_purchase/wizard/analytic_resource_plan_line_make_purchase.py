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

from datetime import datetime
from openerp.osv import fields, osv, orm
from openerp.tools.translate import _


class analytic_resource_plan_line_make_purchase(orm.TransientModel):
    _name = "analytic.resource.plan.line.make.purchase"
    _description = "Resource plan - make purchase"

    def _get_order_lines(self, cr, uid, context=None):
        """
        Returns the order lines associated to the analytic accounts selected.
        """
        if context is None:
            context = {}

        record_ids = context and context.get('active_ids', False)

        if record_ids:
            order_line_ids = []
            line_plan_obj = self.pool.get('analytic.resource.plan.line')

            for line in line_plan_obj.browse(cr, uid, record_ids, context=context):
                    for order_line in line.order_line_ids:
                        order_line_id = order_line and order_line.id
                        order_line_ids.extend([order_line_id])
            if order_line_ids:
                return order_line_ids
        return False

    _columns = {
        'order_line_ids': fields.many2many('purchase.order.line',
                                           'make_purchase_order_line_rel',
                                           'order_line_id',
                                           'make_purchase_order_id'),
    }

    _defaults = {
        'order_line_ids': _get_order_lines,
    }

    def make_purchase_orders(self, cr, uid, ids, context=None):        
        """
             To make purchases.

             @param self: The object pointer.
             @param cr: A database cursor
             @param uid: ID of the user currently logged in
             @param ids: the ID or list of IDs
             @param context: A standard dictionary

             @return: A dictionary which of fields with values.

        """

        if context is None:
            context = {}
        record_ids = context and context.get('active_ids', False)
        res = []
        if record_ids:            
            line_plan_obj = self.pool.get('analytic.resource.plan.line')
            order_obj = self.pool.get('purchase.order')
            order_line_obj = self.pool.get('purchase.order.line')
            partner_obj = self.pool.get('res.partner')                                            
            acc_pos_obj = self.pool.get('account.fiscal.position')           
            
            location_ids = []
            list_line = []
            supplier_data = False
            company_id = False
            purchase_id = False

            for line in line_plan_obj.browse(cr, uid, record_ids, context=context):

                    if not line.supplier_id:
                        raise osv.except_osv(
                            _('Could not create purchase order !'),
                            _('You have to enter a supplier.'))   
                    
                    if supplier_data is not False and line.supplier_id.id != supplier_data:
                        raise osv.except_osv(
                            _('Could not create purchase order !'),
                            _('You have to select lines from the same supplier.'))
                    else:
                        supplier_data = line.supplier_id.id

                    address_id = partner_obj.address_get(cr, uid, [line.supplier_id.id], ['delivery'])['delivery']
                    newdate = datetime.today()
                    partner = line.supplier_id
                    line_company_id = line.company_id and line.company_id.id or False
                    if company_id is not False and line_company_id != company_id:
                        raise osv.except_osv(
                            _('Could not create purchase order !'),
                            _('You have to select lines from the same company.'))
                    else:
                        company_id = line_company_id        
                    
                    line_account_id = line.account_id and line.account_id.id or False

                    account_id = line_account_id
                    
                    warehouse_obj = self.pool.get('stock.warehouse')
                    warehouse_ids = warehouse_obj.search(cr, uid, [('company_id', '=', company_id)])
                    if warehouse_ids:
                        warehouses = warehouse_obj.browse(cr, uid, warehouse_ids, context=context)
                        location_ids = []
                        for lot_stock_ids in warehouses:
                            location_ids.append(lot_stock_ids.lot_stock_id.id)

                    location_id = False
                    if location_ids:
                        location_id = location_ids[0]

                    purchase_order_line = {
                        'name': line.name,
                        'product_qty': line.unit_amount,
                        'product_id': line.product_id.id,
                        'product_uom': line.product_uom_id.id,
                        'price_unit': line.price_unit,
                        'date_planned': line.date,
                        'notes': line.notes,
                        'account_analytic_id': account_id,
                    }
                    taxes = False
                    if line.product_id:
                        taxes_ids = line.product_id.product_tmpl_id.supplier_taxes_id
                        taxes = acc_pos_obj.map_tax(cr, uid, partner.property_account_position, taxes_ids)
                    
                    if taxes:
                        purchase_order_line.update({
                            'taxes_id': [(6, 0, taxes)]
                        })
                    list_line.append(purchase_order_line)
                    
                    if purchase_id is False:
                        purchase_id = order_obj.\
                            create(cr, uid, {'origin': '',
                                             'partner_id': line.supplier_id.id,
                                             'partner_address_id': address_id,
                                             'pricelist_id': line.pricelist_id.id,
                                             'location_id': location_id,
                                             'company_id': company_id,
                                             'fiscal_position': partner.
                                   property_account_position and partner.
                                   property_account_position.id or False,
                                             'payment_term': partner.
                                   property_supplier_payment_term and partner.
                                   property_supplier_payment_term.id or False
                                             }, context=context)
                                                        
                    purchase_order_line.update({
                        'order_id': purchase_id
                    })
                    
                    order_line_id = order_line_obj.create(cr, uid, purchase_order_line, context=context)
                    values = {
                        'order_line_ids': [(4, order_line_id)]
                    }
                    line_plan_obj.write(cr, uid, [line.id], values, context=context)
                    res.append(order_line_id)

        return {
            'domain': "[('id','in', ["+','.join(map(str, res))+"])]",
            'name': _('Purchase order lines'),
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'purchase.order.line',
            'view_id': False,
            'context': False,
            'type': 'ir.actions.act_window'
        }

analytic_resource_plan_line_make_purchase()