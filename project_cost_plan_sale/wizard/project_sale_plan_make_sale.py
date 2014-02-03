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

class project_sale_plan_make_sale(osv.osv_memory):
    _name = "project.sale.plan.make.sale"
    _description = "Project sale plan make sale"
    def make_sales_orders(self, cr, uid, ids, context=None):
        """
             To make sales.

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
            sale_plan_obj = self.pool.get('account.analytic.line.plan')
            #company = self.pool.get('res.users').browse(cr, uid, uid, context).company_id
            order_obj = self.pool.get('sale.order')
            order_line_obj = self.pool.get('sale.order.line')
            partner_obj = self.pool.get('res.partner')                               
            acc_pos_obj = self.pool.get('account.fiscal.position')
            project_obj = self.pool.get('project.project')
                   
            list_line=[]
            sale_order_line={}
            
            customer_data = False
            company_id = False
            account_id = False
            sale_id = False
            price_unit = 0.0
            for line in sale_plan_obj.browse(cr, uid, record_ids, context=context):
                                                        
                    uom_id = line.product_uom_id
                    
                    if not line.customer_id:
                        raise osv.except_osv(
                            _('Could not create sale order !'),
                            _('You have to enter a customer.'))   
                    
                    if customer_data is not False and line.customer_id <> customer_data:
                        raise osv.except_osv(
                        _('Could not create sale order !'),
                        _('You have to select lines from the same customer.'))
                    else:
                        customer_data = line.customer_id
                        
                        
                    partner_addr = partner_obj.address_get(cr, uid, [customer_data.id],
                            ['default', 'invoice', 'delivery', 'contact'])
                    newdate = datetime.today()
                    partner = customer_data
                    pricelist_id = partner.property_product_pricelist and partner.property_product_pricelist.id or False
                    price_unit = line.price_unit

                    line_company_id = line.company_id and line.company_id.id or False
                    if company_id is not False and line_company_id <> company_id:
                        raise osv.except_osv(
                        _('Could not create sale order !'),
                        _('You have to select lines from the same company.'))
                    else:
                        company_id = line_company_id        
                    
                                
                    shop = self.pool.get('sale.shop').search(cr, uid, [('company_id', '=', company_id)])
                    shop_id = shop and shop[0] or False
                    
                    line_account_id = line.account_id and line.account_id.id or False
                    if account_id is not False and line_account_id <> account_id:
                        raise osv.except_osv(
                        _('Could not create sale order !'),
                        _('You have to select lines from the same project.'))
                    else:
                        account_id = line_account_id
                    
                    project_ids = project_obj.search(cr, uid, [('analytic_account_id','=',account_id)])                    
                    project_id = False                    
                    if project_ids:
                        project_id = project_ids[0]
                    else:
                        raise osv.except_osv(
                        _('Cannot create sales order !'),
                        _('No project has been defined for the analytic account.'))        
                   
                    sale_order_line= {
                            'name': line.name,
                            'product_uom_qty': line.unit_amount,
                            'product_id': line.product_id.id,
                            'product_uom': uom_id.id,
                            'price_unit': price_unit,
                            'notes': line.notes,
                            'type': line.product_id.procure_method,                          
                    }
                    taxes_ids = False
                    taxes = False
                    if line.product_id:
                        taxes_ids = line.product_id.product_tmpl_id.taxes_id
                        taxes = acc_pos_obj.map_tax(cr, uid, partner.property_account_position, taxes_ids)
                    
                    if taxes:
                        sale_order_line.update({
                            'tax_id': [(6,0,taxes)]
                            })
                    list_line.append(sale_order_line)
                    
                    if sale_id is False:
                        sale_id = order_obj.create(cr, uid, {
                            'origin': '',
                            'shop_id': shop_id,
                            'partner_id': customer_data.id,
                            'pricelist_id': pricelist_id,
                            'partner_invoice_id': partner_addr['invoice'],
                            'partner_order_id': partner_addr['contact'],
                            'partner_shipping_id': partner_addr['delivery'],
                            'date_order': newdate.strftime('%Y-%m-%d %H:%M:%S'),
                            'fiscal_position': partner.property_account_position and partner.property_account_position.id or False,                            
                            'company_id': company_id,                            
                            'payment_term': partner.property_payment_term and partner.property_payment_term.id or False,
                            'payment_type': partner.payment_type_customer.id,
                            'project': project_id,                        
                        }, context=context)
                                                        
                    sale_order_line.update({
                            'order_id': sale_id
                        })
                    
                    order_line_id = order_line_obj.create(cr,uid,sale_order_line,context=context)    
                    sale_plan_obj.write(cr, uid, [line.id], {'sale_line_id': order_line_id}, context=context)

                           
        return {'type': 'ir.actions.act_window_close'}

project_sale_plan_make_sale()