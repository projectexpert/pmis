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
from openerp.tools.translate import _
from openerp.osv import fields, osv
import openerp.addons.decimal_precision as dp


class analytic_resource_plan_line(osv.osv):

    _name = 'analytic.resource.plan.line'
    _description = "Analytic Resource Planning lines"
    _inherits = {'account.analytic.line.plan': "analytic_line_plan_id"}

    _columns = {
        'supplier_id': fields.many2one('res.partner', 'Supplier', required=False,
                                       domain=[('supplier', '=', True)]),
        'pricelist_id': fields.many2one('product.pricelist',
                                        'Purchasing Pricelist', required=False),
        'price_unit': fields.float('Unit Price', required=False,
                                   digits_compute=dp.get_precision('Purchase Price')),
        'analytic_line_plan_id': fields.many2one('account.analytic.line.plan',
                                                 'Planning analytic lines',
                                                 ondelete="cascade", required=True),
    }

    def on_change_amount_currency_resource(self,
                                           cr, uid, ids, account_id,
                                           name, date, supplier_id,
                                           pricelist_id, product_id, unit_amount,
                                           product_uom_id, price_unit, amount_currency,
                                           currency_id, version_id, journal_id,
                                           ref, company_id, amount, general_account_id, context=None):

        analytic_line_plan_obj = self.pool.get('account.analytic.line.plan')

        res = analytic_line_plan_obj.on_change_amount_currency(cr, uid, ids, amount_currency,
                                                               currency_id, company_id, context)
        return res

    def on_change_currency_resource(self,
                                    cr, uid, ids, account_id,
                                    name, date, supplier_id,
                                    pricelist_id, product_id, unit_amount,
                                    product_uom_id, price_unit, amount_currency,
                                    currency_id, version_id, journal_id,
                                    ref, company_id, amount, general_account_id, context=None):

        return self.on_change_amount_currency_resource(cr, uid, ids, account_id,
                                                       name, date, supplier_id,
                                                       pricelist_id, product_id, unit_amount,
                                                       product_uom_id, price_unit, amount_currency,
                                                       currency_id, version_id, journal_id,
                                                       ref, company_id, amount, general_account_id, context)

    def on_change_unit_amount_resource(self,
                                       cr, uid, ids, account_id,
                                       name, date, supplier_id,
                                       pricelist_id, product_id, unit_amount,
                                       product_uom_id, price_unit, amount_currency,
                                       currency_id, version_id, journal_id,
                                       ref, company_id, amount, general_account_id, context=None):

        res = {}
        res['value'] = {}

        if context is None:
            context = {}

        analytic_line_plan_obj = self.pool.get('account.analytic.line.plan')

        amount_currency = -1 * price_unit * unit_amount
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

    def on_change_price_unit_resource(self,
                                      cr, uid, ids, account_id,
                                      name, date, supplier_id,
                                      pricelist_id, product_id, unit_amount,
                                      product_uom_id, price_unit, amount_currency,
                                      currency_id, version_id, journal_id,
                                      ref, company_id, amount, general_account_id, context=None):

        return self.on_change_unit_amount_resource(cr, uid, ids, account_id,
                                                   name, date, supplier_id,
                                                   pricelist_id, product_id, unit_amount,
                                                   product_uom_id, price_unit, amount_currency,
                                                   currency_id, version_id, journal_id,
                                                   ref, company_id, amount, general_account_id, context)

    def on_change_date_resource(self,
                                cr, uid, ids, account_id,
                                name, date, supplier_id,
                                pricelist_id, product_id, unit_amount,
                                product_uom_id, price_unit, amount_currency,
                                currency_id, version_id, journal_id,
                                ref, company_id, amount, general_account_id, context=None):

        #Change in date affects:
        #  - price_unit => Only if there's a pricelist_id, product_id, product_uom_id and date

        pricelist_obj = self.pool.get('product.pricelist')
        res = {}
        res['value'] = {}

        #Compute new price_unit
        if pricelist_id and product_id and product_uom_id and date:
            price_unit = pricelist_obj.price_get(cr, uid, [pricelist_id],
                                                 product_id, unit_amount or 1.0, supplier_id,
                                                 {'uom': product_uom_id,
                                                  'date': date,
                                                  })[pricelist_id]

            res['value'].update({'price_unit': price_unit})

            res_price_unit = self.on_change_price_unit_resource(cr, uid, ids, account_id,
                                                                name, date, supplier_id,
                                                                pricelist_id, product_id, unit_amount,
                                                                product_uom_id, price_unit, amount_currency,
                                                                currency_id, version_id, journal_id,
                                                                ref, company_id, amount, general_account_id, context)

            if 'value' in res_price_unit:
                res['value'].update(res_price_unit['value'])

        if res['value']:
            return res
        else:
            return {}

    def on_change_account_id_resource(self,
                                      cr, uid, ids, account_id,
                                      name, date, supplier_id,
                                      pricelist_id, product_id, unit_amount,
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

    def on_change_pricelist_id_resource(self,
                                        cr, uid, ids, account_id,
                                        name, date, supplier_id,
                                        pricelist_id, product_id, unit_amount,
                                        product_uom_id, price_unit, amount_currency,
                                        currency_id, version_id, journal_id,
                                        ref, company_id, amount, general_account_id, context=None):

        #Change in pricelist affects price_unit, currency.
        pricelist_obj = self.pool.get('product.pricelist')
        res = {}
        res['value'] = {}

        #Compute new price_unit
        if pricelist_id and product_id and product_uom_id and date:
            price_unit = pricelist_obj.price_get(cr, uid, [pricelist_id],
                                                 product_id, unit_amount or 1.0, supplier_id,
                                                 {'uom': product_uom_id,
                                                  'date': date,
                                                  })[pricelist_id]

            res = self.on_change_price_unit_resource(cr, uid, ids, account_id,
                                                     name, date, supplier_id,
                                                     pricelist_id, product_id, unit_amount,
                                                     product_uom_id, price_unit, amount_currency,
                                                     currency_id, version_id, journal_id,
                                                     ref, company_id, amount, general_account_id, context)
            res['value'].update({'price_unit': price_unit})

        #Compute the new currency
        if pricelist_id:
            pricelist = pricelist_obj.browse(cr, uid, pricelist_id, context=context)
            currency_id = pricelist.currency_id and pricelist.currency_id.id
            res['value'].update({'currency_id': currency_id})

        if res['value']:
            return res
        else:
            return {}

    def on_change_product_uom_resource(self,
                                       cr, uid, ids, account_id,
                                       name, date, supplier_id,
                                       pricelist_id, product_id, unit_amount,
                                       product_uom_id, price_unit, amount_currency,
                                       currency_id, version_id, journal_id,
                                       ref, company_id, amount, general_account_id, context=None):

        res = {}
        res['value'] = {}

        product_obj = self.pool.get('product.product')

        #TODO: Check if the new product is allowed for the current pricelist

        #If there's a pricelist and a product, get the unit price for the new UoM
        if pricelist_id and product_id and product_uom_id:
            res_pricelist = self.on_change_pricelist_id_resource(cr, uid, ids, account_id,
                                                                 name, date, supplier_id,
                                                                 pricelist_id, product_id, unit_amount,
                                                                 product_uom_id, price_unit, amount_currency,
                                                                 currency_id, version_id, journal_id,
                                                                 ref, company_id, amount, general_account_id,
                                                                 context)
            if 'value' in res_pricelist:
                res['value'].update(res_pricelist['value'])

            if 'price_unit' in res['value']:
            #Compute the changes to the price unit downwards
                price_unit = res['value']['price_unit']
                res_price_unit = self.on_change_price_unit_resource(cr, uid, ids, account_id,
                                                                    name, date, supplier_id,
                                                                    pricelist_id, product_id, unit_amount,
                                                                    product_uom_id, price_unit, amount_currency,
                                                                    currency_id, version_id, journal_id,
                                                                    ref, company_id, amount, general_account_id,
                                                                    context)
                if 'value' in res_price_unit:
                    res['value'].update(res_price_unit['value'])

        elif not pricelist_id:
            product = product_obj.browse(cr, uid, product_id, context)
            res['value'].update({'price_unit': product.standard_price})

        if res['value']:
            return res
        else:
            return {}

    def on_change_product_id_resource(self,
                                      cr, uid, ids, account_id,
                                      name, date, supplier_id,
                                      pricelist_id, product_id, unit_amount,
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
            if prod.seller_ids:
                supplier_id = prod.seller_ids[0].name and prod.seller_ids[0].name.id
                res['value'].update({'supplier_id': supplier_id})
                res_supplier = self.onchange_supplier_id(cr, uid, ids, account_id,
                                                         name, date, supplier_id,
                                                         pricelist_id, product_id, unit_amount,
                                                         product_uom_id, price_unit, amount_currency,
                                                         currency_id, version_id, journal_id,
                                                         ref, company_id, amount, general_account_id,
                                                         context)
                res['value'].update(res_supplier['value'])
                if 'pricelist_id' in res_supplier:
                    pricelist_id = res_supplier['pricelist_id']
                if 'currency_id' in res_supplier:
                    currency_id = res_supplier['currency_id']

            prod_uom = prod.uom_po_id and prod.uom_po_id.id or False
            if not prod_uom:
                prod_uom = prod.uom_id and prod.uom_id.id or False
            res['value'].update({'product_uom_id': prod_uom})

            res_uom = self.on_change_product_uom_resource(cr, uid, ids, account_id,
                                                          name, date, supplier_id,
                                                          pricelist_id, product_id, unit_amount,
                                                          prod_uom, price_unit, amount_currency,
                                                          currency_id, version_id, journal_id,
                                                          ref, company_id, amount, general_account_id,
                                                          context)

            res['value'].update(res_uom)

            journal_id = prod.expense_analytic_plan_journal_id and prod.expense_analytic_plan_journal_id.id or False
            res['value'].update({'journal_id': journal_id})

            general_account_id = prod.product_tmpl_id.property_account_expense.id
            if not general_account_id:
                general_account_id = prod.categ_id.property_account_expense_categ.id
            if not general_account_id:
                raise osv.except_osv(_('Error !'),
                                     _('There is no expense account defined '
                                       'for this product: "%s" (id:%d)')
                                     % (prod.name, prod.id,))

            res['value'].update({'general_account_id': general_account_id})

        if res['value']:
            return res
        else:
            return {}

    def onchange_supplier_id(self,
                             cr, uid, ids, account_id,
                             name, date, supplier_id,
                             pricelist_id, product_id, unit_amount,
                             product_uom_id, price_unit, amount_currency,
                             currency_id, version_id, journal_id,
                             ref, company_id, amount, general_account_id, context=None):
        #Change in supplier directly influences
        #  - pricelist
        res = {}
        res['value'] = {}
        pricelist_obj = self.pool.get('product.pricelist')

        if supplier_id:
            partner = self.pool.get('res.partner').browse(cr, uid, supplier_id)
            pricelist_id = partner.property_product_pricelist_purchase and partner.property_product_pricelist_purchase.id
            if pricelist_id:
                res['value'].update({'pricelist_id': pricelist_id})
                res_pricelist = self.on_change_pricelist_id_resource(cr, uid, ids, account_id,
                                                                     name, date, supplier_id,
                                                                     pricelist_id, product_id, unit_amount,
                                                                     product_uom_id, price_unit, amount_currency,
                                                                     currency_id, version_id, journal_id, ref,
                                                                     company_id, amount, general_account_id,
                                                                     context)
                if 'value' in res_pricelist:
                    res['value'].update(res_pricelist['value'])
                pricelist = pricelist_obj.browse(cr, uid, pricelist_id, context=context)
                if pricelist:
                    currency_id = pricelist.currency_id and pricelist.currency_id.id
                    res['value'].update({'currency_id': currency_id})
                    res_currency = self.on_change_currency_resource(cr, uid, ids, account_id,
                                                                    name, date, supplier_id,
                                                                    pricelist_id, product_id, unit_amount,
                                                                    product_uom_id, price_unit, amount_currency,
                                                                    currency_id, version_id, journal_id,
                                                                    ref, company_id, amount, general_account_id,
                                                                    context)
                    if 'value' in res_currency:
                        res['value'].update(res_currency['value'])

        if res['value']:
            return res
        else:
            return {}

    def unlink(self, cr, uid, ids, context=None):
        line_plan_ids = []
        analytic_line_plan_obj = self.pool.get('account.analytic.line.plan')
        for resource_plan_line in self.browse(cr, uid, ids, context=context):
            if resource_plan_line.analytic_line_plan_id:
                line_plan_ids.append(resource_plan_line.analytic_line_plan_id.id)
        res = super(analytic_resource_plan_line, self).unlink(cr, uid, ids, context=context)
        analytic_line_plan_obj.unlink(cr, uid, line_plan_ids, context=context)
        return res

analytic_resource_plan_line()
