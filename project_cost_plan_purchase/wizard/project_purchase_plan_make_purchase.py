# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2011 Eficent (<http://www.eficent.com/>)
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
import time
from datetime import datetime
from osv import osv
from tools.translate import _
import netsvc

class project_purchase_plan_make_purchase(osv.osv_memory):
    _name = "project.purchase.plan.make.purchase"
    _description = "Project purchase plan make purchase"
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
        if record_ids:            
            pur_plan_obj = self.pool.get('account.analytic.line.plan')
            #company = self.pool.get('res.users').browse(cr, uid, uid, context).company_id
            order_obj = self.pool.get('purchase.order')
            order_line_obj = self.pool.get('purchase.order.line')
            partner_obj = self.pool.get('res.partner')                                            
            acc_pos_obj = self.pool.get('account.fiscal.position')
            project_obj = self.pool.get('project.project')
            
            location_ids = []            
            
    
            list_line=[]
            purchase_order_line={}
            
            supplier_data = False
            company_id = False
            account_id = False
            purchase_id = False
            price_unit = 0.0
            for line in pur_plan_obj.browse(cr, uid, record_ids, context=context):
                                                        
                    uom_id = line.product_uom_id
                    
                    if not line.supplier_id:
                        raise osv.except_osv(
                            _('Could not create purchase order !'),
                            _('You have to enter a supplier.'))   
                    
                    if supplier_data is not False and line.supplier_id <> supplier_data:
                        raise osv.except_osv(
                        _('Could not create purchase order !'),
                        _('You have to select lines from the same supplier.'))
                    else:
                        supplier_data = line.supplier_id
                        
                        
                    address_id = partner_obj.address_get(cr, uid, [supplier_data.id], ['delivery'])['delivery']
                    newdate = datetime.today()
                    partner = supplier_data
                    pricelist_id = partner.property_product_pricelist_purchase and partner.property_product_pricelist_purchase.id or False                                        
                    price_unit = line.price_unit
                    line_company_id = line.company_id and line.company_id.id or False  
                    if company_id is not False and line_company_id <> company_id:
                        raise osv.except_osv(
                        _('Could not create purchase order !'),
                        _('You have to select lines from the same company.'))
                    else:
                        company_id = line_company_id        
                    
                    line_account_id = line.account_id and line.account_id.id or False
                    if account_id is not False and line_account_id <> account_id:
                        raise osv.except_osv(
                        _('Could not create purchase order !'),
                        _('You have to select lines from the same analytic account.'))
                    else:
                        account_id = line_account_id
                    
                    
                    project_ids = project_obj.search(cr, uid, [('analytic_account_id','=',account_id)],limit=1)                    
                    project_id = False                    
                    if project_ids:
                        project_id = project_ids[0]
                    else:
                        raise osv.except_osv(
                        _('Cannot create purchase order !'),
                        _('No project has been defined for the analytic account.'))                        
                        
                    warehouse_obj = self.pool.get('stock.warehouse')
                    warehouse_ids = warehouse_obj.search(cr, uid, [('company_id', '=', company_id),])
                    if warehouse_ids:
                        warehouses = warehouse_obj.browse(cr, uid, warehouse_ids, context=context)
                        location_ids = []
                        for lot_stock_ids in warehouses:
                            location_ids.append(lot_stock_ids.lot_stock_id.id)
                    
                    if location_ids:
                        location_id = location_ids[0]
                    
                    #Partner bank                         
                    partner_bank_obj = self.pool.get('res.partner.bank')
                    args = [('partner_id', '=', line.supplier_id.id), ('default_bank', '=', 1)]
                    bank_account_ids = partner_bank_obj.search(cr, uid, args)
                    
                    bank_account_id = False
                    
                    if bank_account_ids:
                        bank_account_id = bank_account_ids[0]
                    
                    purchase_order_line= {
                            'name': line.name,
                            'product_qty': line.unit_amount,
                            'product_id': line.product_id.id,
                            'product_uom': uom_id.id,
                            'price_unit': price_unit,
                            'date_planned': newdate.strftime('%Y-%m-%d %H:%M:%S'),
                            'notes': line.notes,
                            #'notes': product.description_purchase,                            
                    }
                    taxes_ids = False
                    taxes = False
                    if line.product_id:
                        taxes_ids = line.product_id.product_tmpl_id.supplier_taxes_id
                        taxes = acc_pos_obj.map_tax(cr, uid, partner.property_account_position, taxes_ids)
                    
                    if taxes:
                        purchase_order_line.update({
                                'taxes_id': [(6,0,taxes)]
                            })
                    list_line.append(purchase_order_line)
                    
                    if purchase_id is False:
                        purchase_id = order_obj.create(cr, uid, {
                            'origin': '',
                            'partner_id': supplier_data.id,
                            'partner_address_id': address_id,
                            'pricelist_id': pricelist_id,
                            'location_id': location_id,
                            'company_id': company_id,
                            'fiscal_position': partner.property_account_position and partner.property_account_position.id or False,
                            'payment_term': partner.property_payment_term_supplier and partner.property_payment_term_supplier.id or False,
                            'payment_type': partner.payment_type_supplier.id,
                            'project_id': project_id,
                            'partner_bank': bank_account_id
                            #'requisition_id':tender.id,
                            #'notes':tender.description,
                            #'warehouse_id':tender.warehouse_id.id and tender.warehouse_id.id ,
                            #'location_id':location_id,
                            #'company_id':tender.company_id.id,
                        
                        }, context=context)
                                                        
                    purchase_order_line.update({
                            'order_id': purchase_id
                        })
                    
                    order_line_id = order_line_obj.create(cr,uid,purchase_order_line,context=context)    
                    pur_plan_obj.write(cr, uid, [line.id], {'purchase_line_id': order_line_id}, context=context)

                           
        return {'type': 'ir.actions.act_window_close'}

project_purchase_plan_make_purchase()