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
from openerp.osv import fields, osv
from openerp.tools.translate import _


class account_analytic_line_plan(osv.osv):
    _name = 'account.analytic.line.plan'
    _description = 'Analytic planning line'

    def _get_company_currency(self, cr, uid, context=None):
        """
        Returns the default company currency
        """
        if context is None:
            context = {}

        company_obj = self.pool.get('res.company')
        company_id = self.pool.get('res.company')._company_default_get(cr, uid,
                                                             'account.analytic.line',
                                                             context=context)
        company = company_obj.browse(cr, uid, company_id, context=context)
        return company.currency_id and company.currency_id.id or False

    _columns = {
        'name': fields.char('Activity description', size=256, required=True),
        'date': fields.date('Date', required=True, select=True),
        'amount': fields.float('Amount', required=True,
                               help='Calculated by multiplying the quantity '
                                    'and the price given in the Product\'s cost '
                                    'price. Always expressed in the company main '
                                    'currency.',
                               digits_compute=dp.get_precision('Account')),
        'unit_amount': fields.float('Quantity', help='Specifies the amount of quantity to count.'),
        'amount_currency': fields.float('Amount Currency', help="The amount expressed in an optional other currency."),
        'currency_id': fields.many2one('res.currency', 'Currency'),
        'account_id': fields.many2one('account.analytic.account',
                                      'Analytic Account', required=True,
                                      ondelete='cascade', select=True,
                                      domain=[('type', '<>', 'view')]),
        'account_stage': fields.related('account_id', 'stage_id',
                                        type='many2one',
                                        relation='analytic.account.stage',
                                        string='Stage',
                                        readonly=True),
        'user_id': fields.many2one('res.users', 'User'),
        'company_id': fields.related('account_id', 'company_id', type='many2one',
                                     relation='res.company', string='Company',
                                     store=True, readonly=True),
        'product_uom_id': fields.many2one('product.uom', 'UoM'),
        'product_id': fields.many2one('product.product', 'Product'),
        'general_account_id': fields.many2one('account.account', 'General Account',
                                              required=False, ondelete='restrict'),
        'journal_id': fields.many2one('account.analytic.plan.journal',
                                      'Planning Analytic Journal',
                                      required=True, ondelete='restrict',
                                      select=True),
        'code': fields.char('Code', size=8),
        'ref': fields.char('Ref.', size=64),
        'notes': fields.text('Notes'),
        'version_id': fields.many2one('account.analytic.plan.version',
                                      'Planning Version', required=True,
                                      ondelete='cascade'),

    }

    _defaults = {
        'date': lambda *a: time.strftime('%Y-%m-%d'),
        'company_id': lambda self, cr, uid, c: self.pool.get('res.company')._company_default_get(cr, uid,
                                                             'account.analytic.line',
                                                             context=c),
        'currency_id': _get_company_currency,
        'amount': 0.00,
        'journal_id': lambda self, cr, uid,
        context: context['journal_id'] if context and 'journal_id' in context else None,
        'version_id': lambda s, cr, uid,
        c: s.pool.get('account.analytic.plan.version').search(cr, uid,
                                                              [('default_plan', '=', True)],
                                                              context=None),
    }
    _order = 'date desc'

    def search(self, cr, uid, args, offset=0, limit=None, order=None, context=None, count=False):        
        if context is None:
            context = {}
        if context.get('from_date', False):
            args.append(['date', '>=', context['from_date']])
        if context.get('to_date', False):
            args.append(['date', '<=', context['to_date']])
        return super(account_analytic_line_plan, self).search(cr, uid,
                                                              args, offset,
                                                              limit, order,
                                                              context=context,
                                                              count=count)

    def _check_company(self, cr, uid, ids, context=None):
        lines = self.browse(cr, uid, ids, context=context)
        for l in lines:
            if l.move_id and not l.account_id.company_id.id == l.move_id.account_id.company_id.id:
                return False
        return True

    def on_change_amount_currency(self, cr, uid, id, amount_currency, currency_id, company_id, context=None):

        res = {}
        res['value'] = {}

        if context is None:
            context = {}

        currency_obj = self.pool.get('res.currency')
        company_obj = self.pool.get('res.company')

        company = company_obj.browse(cr, uid, company_id, context=context)

        company_currency_id = company.currency_id.id

        if amount_currency:
            amount_company_currency = currency_obj.compute(cr, uid,
                                                           currency_id,
                                                           company_currency_id,
                                                           amount_currency,
                                                           context=context)
        else:
            amount_company_currency = 0.0

        res['value'].update({
            'amount': amount_company_currency,
        })

        return res

    def on_change_unit_amount(self, cr, uid, id, prod_id, quantity, currency_id, company_id,
                              unit=False, journal_id=False, context=None):
                
        res = {}
        
        if context is None:
            context = {}
            
        product_obj = self.pool.get('product.product')
        analytic_journal_obj = self.pool.get('account.analytic.plan.journal')
        product_price_type_obj = self.pool.get('product.price.type')

        prod = False
        if prod_id:
            prod = product_obj.browse(cr, uid, prod_id, context=context)
            res['value'] = {}

        if not journal_id:
            j_ids = analytic_journal_obj.search(cr, uid, [('type', '=', 'purchase')])
            journal_id = j_ids and j_ids[0] or False
        if not journal_id or not prod_id:
            return res
        
        journal = analytic_journal_obj.browse(cr, uid, journal_id, context=context)

        if journal.type != 'sale' and prod:
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

        flag = False
        # Compute based on pricetype
        product_price_type_ids = product_price_type_obj.search(cr, uid,
                                                               [('field', '=', 'standard_price')],
                                                               context=context)
        pricetype = product_price_type_obj.browse(cr, uid, product_price_type_ids,
                                                  context=context)[0]
        if journal_id:
            if journal.type == 'sale':
                product_price_type_ids = product_price_type_obj.search(cr, uid,
                                                                       [('field', '=', 'list_price')],
                                                                       context)
                if product_price_type_ids:
                    pricetype = product_price_type_obj.browse(cr, uid, product_price_type_ids,
                                                              context=context)[0]
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
            
        if not flag:
            if journal.type != 'sale':
                result *= -1

        res = self.on_change_amount_currency(cr, uid, id, result, currency_id, company_id, context)

        res['value'].update({
            'amount_currency': result,
            'general_account_id': a,
        })
        
        return res

    def on_change_product_id(self, cr, uid, id, prod_id, quantity, currency_id, company_id,
                             unit=False, journal_id=False, context=None):
        
        res = self.on_change_unit_amount(cr, uid, id, prod_id, quantity, currency_id, company_id,
                                         unit, journal_id, context)

        prod = self.pool.get('product.product').browse(cr, uid, prod_id, context=context)
        if prod:
            if prod.uom_po_id:
                res['value'].update({
                    'product_uom_id': prod.uom_po_id.id,
                })
            elif prod.uom_id:
                res['value'].update({
                    'product_uom_id': prod.uom_id.id,
                })

        return res  

    def view_header_get(self, cr, user, view_id, view_type, context=None):
        if context is None:
            context = {}
        if context.get('account_id', False):
            # account_id in context may also be pointing to an account.account.id
            cr.execute('select name from account_analytic_account where id=%s', (context['account_id'],))
            res = cr.fetchone()
            if res:
                res = _('Entries: ')+(res[0] or '')
            return res

        return False

account_analytic_line_plan()