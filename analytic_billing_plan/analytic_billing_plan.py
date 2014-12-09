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
import openerp.addons.decimal_precision as dp
from openerp.tools.translate import _
from openerp.osv import fields, osv


class analytic_billing_plan_line(osv.osv):

    _name = 'analytic.billing.plan.line'
    _description = "Analytic Billing Plan lines"
    _inherits = {'account.analytic.line.plan': "analytic_line_plan_id"}

    def _has_active_order(self, cr, uid, ids, fields, arg, context=None):
        res = {}
        if context is None:
            context = {}

        for plan_line in self.browse(cr, uid, ids, context=context):
            res[plan_line.id] = False
            for order_line in plan_line.order_line_ids:
                if order_line.state and order_line.state != 'cancel':
                    res[plan_line.id] = True
        return res

    _columns = {
        'price_unit': fields.float('Unit Price', required=False, digits_compute=dp.get_precision('Sale Price')),
        'customer_id': fields.related('account_id', 'partner_id', string="Customer",
                                      type='many2one', readonly=True, relation="res.partner"),
        'analytic_line_plan_id': fields.many2one('account.analytic.line.plan',
                                                 'Planning analytic lines', ondelete="cascade",
                                                 required=True),

        'order_line_ids': fields.many2many('sale.order.line',
                                           'analytic_billing_plan_order_line_rel',
                                           'order_line_id',
                                           'analytic_billing_plan_line_id'),
        'has_active_order': fields.function(_has_active_order,
                                            method=True,
                                            type='boolean',
                                            string='Billing request',
                                            help="Indicates that this billing plan line "
                                                 "contains at least one non-cancelled billing request."),
    }

    def on_change_amount_currency_billing(self,
                                          cr, uid, ids, account_id,
                                          name, date, product_id, unit_amount,
                                          product_uom_id, price_unit, amount_currency,
                                          currency_id, version_id, journal_id,
                                          ref, company_id, amount, general_account_id, context=None):

        analytic_line_plan_obj = self.pool.get('account.analytic.line.plan')

        res = analytic_line_plan_obj.on_change_amount_currency(cr, uid, ids, amount_currency,
                                                               currency_id, company_id, context)
        return res

    def on_change_currency_billing(self,
                                   cr, uid, ids, account_id,
                                   name, date, product_id, unit_amount,
                                   product_uom_id, price_unit, amount_currency,
                                   currency_id, version_id, journal_id,
                                   ref, company_id, amount, general_account_id, context=None):

        return self.on_change_amount_currency_billing(cr, uid, ids, account_id,
                                                      name, date, product_id, unit_amount,
                                                      product_uom_id, price_unit, amount_currency,
                                                      currency_id, version_id, journal_id,
                                                      ref, company_id, amount, general_account_id, context)

    def on_change_unit_amount_billing(self,
                                      cr, uid, ids, account_id,
                                      name, date, product_id, unit_amount,
                                      product_uom_id, price_unit, amount_currency,
                                      currency_id, version_id, journal_id,
                                      ref, company_id, amount, general_account_id, context=None):

        res = {}
        res['value'] = {}

        if context is None:
            context = {}

        analytic_line_plan_obj = self.pool.get('account.analytic.line.plan')

        amount_currency = price_unit * unit_amount
        res['value'].update({'amount_currency': amount_currency})

        res_amount_currency = analytic_line_plan_obj.on_change_amount_currency(cr, uid, ids,
                                                                               amount_currency, currency_id,
                                                                               company_id, context)
        if res_amount_currency and 'value' in res_amount_currency:
            res['value'].update(res_amount_currency['value'])

        if res['value']:
            return res
        else:
            return {}

    def on_change_price_unit_billing(self,
                                     cr, uid, ids, account_id,
                                     name, date, product_id, unit_amount,
                                     product_uom_id, price_unit, amount_currency,
                                     currency_id, version_id, journal_id,
                                     ref, company_id, amount, general_account_id, context=None):

        return self.on_change_unit_amount_billing(cr, uid, ids, account_id,
                                                  name, date, product_id, unit_amount,
                                                  product_uom_id, price_unit, amount_currency,
                                                  currency_id, version_id, journal_id,
                                                  ref, company_id, amount, general_account_id, context)

    def on_change_date_billing(self,
                               cr, uid, ids, account_id,
                               name, date, product_id, unit_amount,
                               product_uom_id, price_unit, amount_currency,
                               currency_id, version_id, journal_id,
                               ref, company_id, amount, general_account_id, context=None):

        res = {}
        res['value'] = {}

        if res['value']:
            return res
        else:
            return {}

    def on_change_account_id_billing(self,
                                     cr, uid, ids, account_id,
                                     name, date, product_id, unit_amount,
                                     product_uom_id, price_unit, amount_currency,
                                     currency_id, version_id, journal_id,
                                     ref, company_id, amount, general_account_id, context=None):
        res = {}
        res['value'] = {}
        #Change in account_id affects:
        #  - version_id
        analytic_obj = self.pool.get('account.analytic.account')
        if account_id:
            analytic = analytic_obj.browse(cr, uid, account_id, context)
            version_id = analytic.active_analytic_planning_version and analytic.active_analytic_planning_version.id or False
            res['value'].update({'version_id': version_id})

        if res['value']:
            return res
        else:
            return {}

    def on_change_product_uom_billing(self,
                                      cr, uid, ids, account_id,
                                      name, date, product_id, unit_amount,
                                      product_uom_id, price_unit, amount_currency,
                                      currency_id, version_id, journal_id,
                                      ref, company_id, amount, general_account_id, context=None):

        analytic_account_obj = self.pool.get('account.analytic.account')
        partner_obj = self.pool.get('res.partner')
        product_obj = self.pool.get('product.product')
        pricelist_obj = self.pool.get('product.pricelist')

        res = {}
        res['value'] = {}

        analytic_account = analytic_account_obj.browse(cr, uid, account_id, context=context)
        customer_id = analytic_account.partner_id and analytic_account.partner_id.id
        customer = partner_obj.browse(cr, uid, customer_id, context=context)
        pricelist_id = customer.property_product_pricelist and customer.property_product_pricelist.id or False

        #TODO: Check if the new product is allowed for the current pricelist
        #If there's a pricelist and a product, get the unit price for the new UoM
        if pricelist_id and product_id and product_uom_id:
            price_unit = pricelist_obj.price_get(cr, uid, [pricelist_id],
                                                 product_id, unit_amount or 1.0, customer_id,
                                                 {'uom': product_uom_id,
                                                  'date': date,
                                                  })[pricelist_id]
            res['value'].update({'price_unit': price_unit})

            if 'price_unit' in res['value']:
            #Compute the changes to the price unit downwards
                price_unit = res['value']['price_unit']
                res_price_unit = self.on_change_price_unit_billing(cr, uid, ids, account_id,
                                                                   name, date, product_id, unit_amount,
                                                                   product_uom_id, price_unit, amount_currency,
                                                                   currency_id, version_id, journal_id,
                                                                   ref, company_id, amount, general_account_id,
                                                                   context)
                if 'value' in res_price_unit:
                    res['value'].update(res_price_unit['value'])

        elif not pricelist_id:
            product = product_obj.browse(cr, uid, product_id, context)
            res['value'].update({'price_unit': product.list_price})

        if res['value']:
            return res
        else:
            return {}

    def on_change_product_id_billing(self,
                                     cr, uid, ids, account_id,
                                     name, date, product_id, unit_amount,
                                     product_uom_id, price_unit, amount_currency,
                                     currency_id, version_id, journal_id,
                                     ref, company_id, amount, general_account_id, context=None):
        #Change in product allowed only if:
        #  - Compatible with current pricelist? => TODO
        #Change in product directly influences
        #  - UoM, only if there's no pricelist
        #  - journal_id
        #  - general_account_id

        res = {}
        res['value'] = {}

        if product_id:
            prod = self.pool.get('product.product').browse(cr, uid, product_id, context=context)
            prod_uom = prod.uos_id and prod.uos_id.id or False
            if not prod_uom:
                prod_uom = prod.uom_id and prod.uom_id.id or False
            res['value'].update({'product_uom_id': prod_uom})

            res_uom = self.on_change_product_uom_billing(cr, uid, ids, account_id,
                                                         name, date, product_id, unit_amount,
                                                         prod_uom, price_unit, amount_currency,
                                                         currency_id, version_id, journal_id,
                                                         ref, company_id, amount, general_account_id,
                                                         context)

            res['value'].update(res_uom)

            journal_id = prod.revenue_analytic_plan_journal_id and prod.revenue_analytic_plan_journal_id.id or False
            res['value'].update({'journal_id': journal_id})

            general_account_id = prod.product_tmpl_id.property_account_income.id
            if not general_account_id:
                general_account_id = prod.categ_id.property_account_income_categ.id
            if not general_account_id:
                    raise osv.except_osv(_('Error !'),
                                         _('There is no income account defined '
                                           'for this product: "%s" (id:%d)')
                                         % (prod.name, product_id,))

            res['value'].update({'general_account_id': general_account_id})

        if res['value']:
            return res
        else:
            return {}
           
    def unlink(self, cr, uid, ids, context=None):
        line_plan_ids = []
        analytic_line_plan_obj = self.pool.get('account.analytic.line.plan')
        for billing_plan_line in self.browse(cr, uid, ids, context=context):
            if billing_plan_line.analytic_line_plan_id:
                line_plan_ids.append(billing_plan_line.analytic_line_plan_id.id)
        res = super(analytic_billing_plan_line, self).unlink(cr, uid, ids, context=context)
        analytic_line_plan_obj.unlink(cr, uid, line_plan_ids, context=context)
        return res

analytic_billing_plan_line()