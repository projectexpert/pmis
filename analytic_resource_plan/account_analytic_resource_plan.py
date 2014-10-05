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

import time
from tools.translate import _
from openerp.osv import fields, osv
import decimal_precision as dp


class account_analytic_resource_plan_line(osv.osv):

    _name = 'account.analytic.resource.plan.line'
    _description = "Analytic Resource Planning lines"
    _inherits = {'account.analytic.line.plan': "analytic_line_plan_id"}

    _columns = {
        'supplier_id': fields.many2one('res.partner', 'Supplier', required=False, domain=[('supplier', '=', True)]),
        'pricelist_id': fields.many2one('product.pricelist', 'Purchasing Pricelist', required=False),
        'price_unit': fields.float('Purchasing Unit Price', required=False, digits_compute= dp.get_precision('Purchase Price')),
        'analytic_line_plan_id': fields.many2one('account.analytic.line.plan', 'Planning analytic lines', ondelete="cascade", required=True),
    }

    def get_general_account_id_resource(self, cr, uid, id, prod_id, qty, company_id,
                                        unit=False, journal_id=False, context=None):

        result = False
        
        product_obj = self.pool.get('product.product')
        
        if prod_id:
            prod = product_obj.browse(cr, uid, prod_id, context=context)
                                
            if not journal_id:
                j_ids = self.pool.get('account.analytic.plan.journal').search(cr,
                                                                              uid, 
                                                                              [('type', '=', 'purchase')])
                journal_id = j_ids and j_ids[0] or False
            if not journal_id or not prod_id:
                return result
            
            analytic_journal_obj = self.pool.get('account.analytic.plan.journal')
            j_id = analytic_journal_obj.browse(cr, uid, journal_id, context=context)
              
            if j_id.type != 'sale':
                a = prod.product_tmpl_id.property_account_expense.id
                if not a:
                    a = prod.categ_id.property_account_expense_categ.id
                if not a:
                    raise osv.except_osv(_('Error !'),
                                         _('There is no expense account defined '
                                           'for this product: "%s" (id:%d)') 
                                         % (prod.name, prod.id,))
            else:
                a = prod.product_tmpl_id.property_account_income.id
                if not a:
                    a = prod.categ_id.property_account_income_categ.id
                if not a:
                    raise osv.except_osv(_('Error !'), 
                                         _('There is no income account defined '
                                           'for this product: "%s" (id:%d)') 
                                         % (prod.name, prod_id,))
            
            result = a
        return result        

    def on_change_price_unit(self, cr, uid, id,
                             price_unit,
                             unit_amount,
                             context=None):
        res = {}
        amount_currency = -1 * price_unit * unit_amount

        vals = {'amount_currency': amount_currency}

        if 'value' in res:
            res['value'].update(vals)
        else:
            res.update({'value': vals})

        return res

    def on_change_unit_amount_resource(self, cr, uid, id,                                         
                                       product_id, 
                                       partner_id,
                                       pricelist_id,
                                       unit_amount, 
                                       currency_id, 
                                       company_id,
                                       product_uom_id=False, 
                                       journal_id=False, 
                                       context=None):    
                
        if context is None:
            context = {}

        analytic_line_plan_obj = self.pool.get('account.analytic.line.plan')
        pricelist_obj = self.pool.get('product.pricelist')

        res = analytic_line_plan_obj.on_change_unit_amount(cr, uid, id, 
                                                           product_id,
                                                           unit_amount,
                                                           currency_id,
                                                           company_id,
                                                           product_uom_id,
                                                           journal_id,
                                                           context)

        if pricelist_id and product_id and product_uom_id:
            price_unit = pricelist_obj.price_get(cr, uid, [pricelist_id],
                                                 product_id, unit_amount or 1.0, partner_id,
                                                 {'uom': product_uom_id,
                                                  'date': time.strftime('%Y-%m-%d'),
                                                  })[pricelist_id]
            pricelist = pricelist_obj.browse(cr, uid, pricelist_id, context=context)

            amount_currency = -1 * price_unit * unit_amount

            res = analytic_line_plan_obj.on_change_amount_currency(cr, uid, id,
                                                                   amount_currency,
                                                                   currency_id,
                                                                   company_id,
                                                                   context)

            currency_id = pricelist.currency_id and pricelist.currency_id.id

            res['value'].update({
                'price_unit': price_unit,
                'amount_currency': amount_currency,
                'currency_id': currency_id,
            })
            
        return res
                            
    def on_change_product_uom_resource(self, cr, uid, ids, pricelist_id, product_id,
                                       company_id, unit_amount, currency_id, product_uom_id,
                                       journal_id, supplier_id, date, context=None):
        
        res = self.on_change_product_id_resource(cr, uid, ids, pricelist_id, product_id,
                                                 company_id, unit_amount, currency_id, product_uom_id,
                                                 journal_id, supplier_id, context)
        
        if 'product_uom_id' in res['value']:
            if product_uom_id and (product_uom_id != res['value']['product_uom_id']) \
                    and res['value']['product_uom_id']:
                seller_uom_name = self.pool.get('product.uom').read(cr, uid,
                                                                    [res['value']['product_uom_id']],
                                                                    ['name'])[0]['name']
                res.update({'warning': {'title': _('Warning'),
                                        'message': _('The selected supplier '
                                                     'only sells this product by %s') % seller_uom_name}})
            del res['value']['product_uom_id']

        return res    
    
    def onchange_supplier_id(self, cr, uid, ids, product_id, company_id, qty,
                             currency_id, uom, journal_id, partner_id, context=None):
        pricelist_id = False
        pricelist_obj = self.pool.get('product.pricelist')

        if partner_id:
            partner = self.pool.get('res.partner').browse(cr, uid, partner_id)
            pricelist_id = partner.property_product_pricelist_purchase and partner.property_product_pricelist_purchase.id
            pricelist = pricelist_obj.browse(cr, uid, pricelist_id, context=context)

            currency_id = pricelist.currency_id and pricelist.currency_id.id

        res = self.on_change_product_id_resource(cr, uid, ids, pricelist_id, product_id, company_id,
                                                 qty, currency_id, uom, journal_id, partner_id, context)

        res['value'].update({
            'pricelist_id': pricelist_id,
            'currency_id': currency_id,
        })
        
        return res

    def on_change_product_id_resource(self, cr, uid, ids, pricelist, product_id,
                                      company_id, qty, currency_id, uom, journal_id,
                                      partner_id, context=None):

        general_account_id = False
        journal_id = False

        if product_id:
            prod = self.pool.get('product.product').browse(cr, uid, product_id, context=context)
            prod_uom_po = prod.uom_po_id and prod.uom_po_id.id or False
            journal_id = prod.expense_analytic_plan_journal_id and prod.expense_analytic_plan_journal_id.id or False

            general_account_id = self.get_general_account_id_resource(cr,
                                                                      uid,
                                                                      ids,
                                                                      product_id,
                                                                      qty,
                                                                      company_id,
                                                                      uom,
                                                                      journal_id,
                                                                      context)

        else:
            prod_uom_po = uom

        res = self.on_change_unit_amount_resource(cr, uid, id,
                                                  product_id,
                                                  partner_id,
                                                  pricelist,
                                                  qty,
                                                  currency_id,
                                                  company_id,
                                                  prod_uom_po,
                                                  journal_id,
                                                  context)

        vals = {
            'product_uom_id': prod_uom_po,
            'general_account_id': general_account_id,
            'journal_id': journal_id,
        }

        if 'value' in res:
            res['value'].update(vals)
        else:
            res.update({'value': vals})

        return res

    def unlink(self, cr, uid, ids, context=None):
        line_plan_ids = []
        analytic_line_plan_obj = self.pool.get('account.analytic.line.plan')
        for resource_plan_line in self.browse(cr, uid, ids, context=context):
            if resource_plan_line.analytic_line_plan_id:
                line_plan_ids.append(resource_plan_line.analytic_line_plan_id.id)
        res = super(account_analytic_resource_plan_line, self).unlink(cr, uid, ids, context=context)
        analytic_line_plan_obj.unlink(cr, uid, line_plan_ids, context=context)
        return res

account_analytic_resource_plan_line()
