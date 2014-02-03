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

from lxml import etree
import time
from datetime import datetime, date, timedelta
import decimal_precision as dp
from tools.translate import _
from osv import fields, osv
import netsvc
import tools


class account_analytic_line_plan(osv.osv):

    _inherit = 'account.analytic.line.plan'

    _columns = {
        'sale_line_id': fields.many2one('sale.order.line', 'Sale Order Line', select=True),
        'sale_order_id':fields.related('sale_line_id', 'order_id', type='many2one' , relation='sale.order', string='Sale Order', store=True, readonly=True),
        'customer_id': fields.many2one('res.partner', 'Customer', requrired=False ,domain=[('customer', '=', True)]),
        'pricelist_id':fields.many2one('product.pricelist', 'Pricelist', required=False),
        'price_unit': fields.float('Unit Price', required=True, digits_compute= dp.get_precision('Sale Price')),
        'sale_amount': fields.float('Sale Amount', required=True, digits_compute= dp.get_precision('Sale Price')),                
    }

      
    def copy(self, cr, uid, id, default={}, context=None):
        if context is None:
            context = {}
        
        if not default:
            default = {}   
        
        default['sale_line_id'] = False
                
        res = super(account_analytic_line_plan, self).copy(cr, uid, id, default, context)
        return res
    
    def copy_data(self, cr, uid, id, default={}, context=None):

        if context is None:
            context = {}
        if not default:
            default = {}   
            
        default['sale_line_id'] = False
                
        res = super(account_analytic_line_plan, self).copy_data(cr, uid, id, default, context)
        return res
    
        
    def on_change_sale_amount(self, cr, uid, id, sale_amount, context=None):
        
        result = {'amount': 1 * sale_amount }
        
        return {'value': result}    
    
        # Compute the cost based on the price type define into company
    # property_valuation_price_type property
    def get_general_account_id(self, cr, uid, id, prod_id, qty, company_id,
            unit=False, journal_id=False, context=None):

        result = False
        
        product_obj = self.pool.get('product.product')
        
        if prod_id:
            prod = product_obj.browse(cr, uid, prod_id, context=context)
                                
        if not journal_id:
            j_ids = self.pool.get('account.analytic.journal.plan').search(cr, uid, [('type','=','sale')], context=context)
            journal_id = j_ids and j_ids[0] or False
        if not journal_id or not prod_id:
            return result
        
        analytic_journal_obj =self.pool.get('account.analytic.journal.plan')
        j_id = analytic_journal_obj.browse(cr, uid, journal_id, context=context)
                
        if j_id.type <> 'sale':
            a = prod.product_tmpl_id.property_account_expense.id
            if not a:
                a = prod.categ_id.property_account_expense_categ.id
            if not a:
                raise osv.except_osv(_('Error !'),
                        _('There is no expense account defined ' \
                                'for this product: "%s" (id:%d)') % \
                                (prod.name, prod.id,))
        else:
            a = prod.product_tmpl_id.property_account_income.id
            if not a:
                a = prod.categ_id.property_account_income_categ.id
            if not a:
                raise osv.except_osv(_('Error !'),
                        _('There is no income account defined ' \
                                'for this product: "%s" (id:%d)') % \
                                (prod.name, prod_id,))
        
        result = a
        return result        
        
    def on_change_unit_amount_sale(self, cr, uid, id, price, prod_id, qty, company_id,
            unit=False, journal_id=False, context=None):
                
        if context==None:
            context={}
            
        sale_amount = price * qty
        amount = 1*price * qty   
        
        
        result = {
            'sale_amount': sale_amount,
            'amount': amount,            
            }
        return {'value': result}
                            
    def product_uom_change_sale(self, cr, uid, ids, pricelist, product, company_id, qty, uom, price, journal_id,
        partner_id, price_unit=False):
        
        res = self.product_id_change_sale(cr, uid, ids, pricelist, product, company_id, qty, uom, price, journal_id,
                partner_id, date=date, price_unit=price_unit)
        
        if 'product_uom_id' in res['value']:
            del res['value']['product_uom_id']
        if not uom:
            res['value']['price_unit'] = 0.0
        return res
    
    def onchange_customer_id(self, cr, uid, ids, part):
        
        pricelist = False
        
        if part:
            part = self.pool.get('res.partner').browse(cr, uid, part)
            pricelist = part.property_product_pricelist and part.property_product_pricelist.id
                    
        result = {'pricelist_id': pricelist}
        return {'value': result}

    def product_id_change_sale(self, cr, uid, ids, pricelist, product, company_id, qty, uom, price, journal_id,
            partner_id, date=False, price_unit=False):

        if not product:
            return {'value': {'price_unit': price_unit or 0.0,
                'product_uom_id' : uom or False}, 'domain':{'product_uom_id':[]}}

        general_account_id = self.get_general_account_id(cr, uid, id, product, qty, company_id, uom, journal_id)

        
        product_uom_pool = self.pool.get('product.uom')
        lang=False
        if partner_id:
            lang=self.pool.get('res.partner').read(cr, uid, partner_id, ['lang'])['lang']
        context={'lang':lang}
        context['partner_id'] = partner_id

        prod = self.pool.get('product.product').browse(cr, uid, product, context=context)
        prod_uom_po = prod.uom_po_id.id
        if not uom:
            uom = prod_uom_po
       
        qty = qty or 1.0
        
        prod_name = prod.name
        res = {}        
        qty_in_product_uom = product_uom_pool._compute_qty(cr, uid, uom, qty, to_uom_id=prod.uom_id.id)
        
        if pricelist:
            price = self.pool.get('product.pricelist').price_get(cr,uid,[pricelist],
                    product, qty_in_product_uom or 1.0, partner_id, {
                        'uom': uom,
                        'date': time.strftime('%Y-%m-%d'),
                        })[pricelist]
        else:
            price = price
             
        sale_amount = price * qty
        amount = -1*price * qty   
                  
        res.update({'value': {
            'price_unit': price, 
            'name': prod_name,
            'unit_amount': qty,
            'product_uom_id': uom,
            'sale_amount': sale_amount,
            'amount': amount,
            'general_account_id': general_account_id
            }})
        
        return res    
    
    
account_analytic_line_plan()

