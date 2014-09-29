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

import openerp.addons.decimal_precision as dp
from openerp.tools.translate import _
from openerp.osv import fields, osv


class account_analytic_line_plan(osv.osv):

    _inherit = 'account.analytic.line.plan'

        
    _columns = {

        'employee_id': fields.many2one('hr.employee', 'Employee', requrired=False),
        'time_amount': fields.float('Time Amount', required=True, digits_compute= dp.get_precision('Amount')),
                
    }

    def on_change_time_amount(self, cr, uid, id, time_amount, context=None):
        
        result = {'amount': -1 * time_amount }
        
        return {'value': result}    
    

    def product_uom_change_time(self, cr, uid, ids, product, company_id, qty, uom, price, journal_id,
        employee_id):
        
        res = self.product_id_change_time(cr, uid, ids, product, company_id, qty, uom, price, journal_id,
                employee_id)
        
        if 'product_uom_id' in res['value']:
            if uom and (uom != res['value']['product_uom_id']) and res['value']['product_uom_id']:
                seller_uom_name = self.pool.get('product.uom').read(cr, uid, [res['value']['product_uom_id']], ['name'])[0]['name']
                res.update({'warning': {'title': _('Warning'), 'message': _('The selected supplier only sells this product by %s') % seller_uom_name }})
            del res['value']['product_uom_id']

        return res    
    
    def on_change_employee_id(self, cr, uid, ids, product, company_id, qty, uom, price, journal_id,
                employee_id, context=None):

        result = {}
        if context is None:
            context = {}
        
        lang_dict = self.pool.get('res.users').read(cr,uid,uid,['context_lang'])
        
        context.update({'lang': lang_dict.get('context_lang')})
                        
        if employee_id:
            emp = self.pool.get('hr.employee').browse(cr, uid, employee_id, context)        
            if emp.product_id:
                result = self.product_id_change_time(cr, uid, ids, emp.product_id.id, company_id, qty, uom, price, journal_id,
                employee_id, context)
                
        return result

    def product_id_change_time(self, cr, uid, ids, product, company_id, qty, uom, price, journal_id,
            employee_id, context=None):

        res = {}
        if not product:
            return res
        
        prod = self.pool.get('product.product').browse(cr, uid, product, context)
        prod_uom_po = prod.uom_po_id.id
        if not uom:
            uom = prod_uom_po
       
        qty = qty or 1.0
        prod_name = prod.name
        
        result = self.on_change_unit_amount_time(cr, uid, id, product, qty, company_id, uom, journal_id, context=None)
        
 
        res.update({'value': {
            'name': prod_name,            
            'product_id':product,
            'product_uom_id': uom,
            'unit_amount': qty,
            'amount': result['value']['amount'],
            'time_amount': result['value']['time_amount'],
            'general_account_id': result['value']['general_account_id'],
            }})
        
        return res    

    # Compute the cost based on the price type define into company
    # property_valuation_price_type property
    def on_change_unit_amount_time(self, cr, uid, id, prod_id, quantity, company_id,
            unit=False, journal_id=False, context=None):
        
        res={}
        
        if context==None:
            context={}
            
        product_obj = self.pool.get('product.product')
        
        if prod_id:
            prod = product_obj.browse(cr, uid, prod_id, context=context)
            res['value']={ }
#                          'product_uom_id': prod.uom_id.id,
#                          'unit_amount': quantity or 1.0
#                          }
                                
        if not journal_id:
            j_ids = self.pool.get('account.analytic.journal.plan').search(cr, uid, [('type','=','general')])
            journal_id = j_ids and j_ids[0] or False
        if not journal_id or not prod_id:
            return res
        
        analytic_journal_obj =self.pool.get('account.analytic.journal.plan')
        product_price_type_obj = self.pool.get('product.price.type')
        j_id = analytic_journal_obj.browse(cr, uid, journal_id, context=context)
        
        result = 0.0

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

        flag = False
        # Compute based on pricetype
        product_price_type_ids = product_price_type_obj.search(cr, uid, [('field','=','standard_price')], context=context)
        pricetype = product_price_type_obj.browse(cr, uid, product_price_type_ids, context=context)[0]
        if journal_id:
            journal = analytic_journal_obj.browse(cr, uid, journal_id, context=context)
            if journal.type == 'sale':
                product_price_type_ids = product_price_type_obj.search(cr, uid, [('field','=','list_price')], context)
                if product_price_type_ids:
                    pricetype = product_price_type_obj.browse(cr, uid, product_price_type_ids, context=context)[0]
        # Take the company currency as the reference one
        if pricetype.field == 'list_price':
            flag = True
        ctx = context.copy()
        if unit:
            # price_get() will respect a 'uom' in its context, in order
            # to return a default price for those units
            ctx['uom'] = unit
        amount_unit = prod.price_get(pricetype.field, context=ctx)[prod.id]
        prec = self.pool.get('decimal.precision').precision_get(cr, uid, 'Account')
        amount = amount_unit * quantity or 1.0
        result = round(amount, prec)
            

        res['value'].update({
            'amount': -1*result,
            'time_amount': result,
            'general_account_id': a,
            })
        
        return res
    
    
account_analytic_line_plan()

