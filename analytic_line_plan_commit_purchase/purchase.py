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
from openerp.osv import osv, fields
from openerp.tools.translate import _


class purchase_order(osv.osv):

    _inherit = 'purchase.order'


def write(self, cr, uid, ids, data, context=None):
    if context is None:
        context = {}

    po_line_obj = self.pool.get('purchase.order.line')
    line_plan_obj = self.pool.get('account.analytic.line.plan')
    currency_obj = self.pool.get('res.currency')

    for po in self.browse(cr, uid, ids, context=context):
        vals_line = {}
        for order_line_id in po.order_line:
            for order_line in po_line_obj.browse(
                cr, uid, [order_line_id.id], context=context
            ):
                if order_line.analytic_line_plan:

                    crx = po.currency_id

                    if 'state' in data:

                        if data['state'] in (
                            'approved',
                            'except_picking',
                            'except_invoice',
                            'done'
                        ):

                            if crx.id != (
                                po.company_id.currency_id.id
                            ):
                                amount_company_currency = (
                                    currency_obj.compute(
                                        cr,
                                        uid,
                                        crx.id,
                                        po.company_id.currency_id.id,
                                        order_line.price_subtotal,
                                        context=context
                                    )
                                )
                            else:

                                olpsx = order_line.price_subtotal

                                amount_company_currency = olpsx

                            vals_line['amount_currency'] = -1 * olpsx
                            if po.currency_id:
                                vals_line['currency_id'] = po.currency_id.id
                            vals_line['amount'] = -1 * amount_company_currency
                            vals_line['unit_amount'] = order_line.product_qty
                        else:
                            vals_line['amount'] = 0
                            vals_line['unit_amount'] = 0
                    if 'company_id' in data:
                        vals_line['company_id'] = data['company_id']

                    line_plan_obj.write(
                        cr, uid,
                        [order_line.analytic_line_plan.id],
                        vals_line,
                        context
                    )

    return super(purchase_order, self).write(
        cr, uid, ids, data, context=context
    )

    return super(purchase_order, self).write(
        cr, uid, ids, data, context=context
    )

purchase_order()


class purchase_order_line(osv.osv):

    _inherit = 'purchase.order.line'

    _columns = {
        'analytic_line_plan': fields.many2one(
            'account.analytic.line.plan',
            'Planning Analytic line'
        ),
    }

    def create(self, cr, uid, vals, *args, **kwargs):
        purchase_order_obj = self.pool.get('purchase.order')
        line_plan_obj = self.pool.get('account.analytic.line.plan')
        plan_version_obj = self.pool.get('account.analytic.plan.version')
        plan_journal_obj = self.pool.get('account.analytic.plan.journal')
        product_obj = self.pool.get('product.product')
        vals_line = {}
        context = kwargs.get('context', {})

        if 'analytic_line_plan' in vals:
            version_id = plan_version_obj.search(
                cr, uid, [('default_committed', '=', True)], context=context
            )[0]
            if not version_id:
                raise osv.except_osv(
                    _('Error!'),
                    _(
                        'Please define an analytic planning version '
                        'as default for committed costs.'
                    )
                )

            j_ids = plan_journal_obj.search(
                cr, uid, [('type', '=', 'purchase')]
            )
            journal_id = j_ids and j_ids[0] or False
            if not journal_id:
                raise osv.except_osv(
                    _(
                        'Error!'
                    ),
                    _(
                        'Please define an analytic planning journal'
                        'for purchases.'
                    )
                )

            order = False
            if 'order_id' in vals:
                order = purchase_order_obj.browse(
                    cr, uid, vals['order_id'], context=context
                )
                if order.currency_id:
                    vals_line['currency_id'] = order.currency_id.id

            general_account_id = False
            if 'product_id' in vals:
                prod = product_obj.browse(
                    cr, uid, vals['product_id'], context=context
                )

                pptix = prod.product_tmpl_id
                pcpaecx = prod.categ_id.property_account_expense_categ

                general_account_id = pptix.property_account_expense.id
                if not general_account_id:
                    general_account_id = pcpaecx.id
                if not general_account_id:
                    raise osv.except_osv(
                        _('Error !'),
                        _('There is no expense account defined '
                          'for this product: "%s" (id:%d)')
                        % (prod.name, prod.id,))

            vals_line['name'] = vals['name']
            vals_line['date'] = vals['date_planned']
            vals_line['amount'] = 0
            vals_line['amount_currency'] = 0
            vals_line['unit_amount'] = 0
            vals_line['account_id'] = vals['account_analytic_id']
            vals_line['company_id'] = (
                order.company_id and
                order.company_id.id
            )
            vals_line['product_uom_id'] = vals['product_uom']
            vals_line['product_id'] = vals['product_id']
            vals_line['version_id'] = version_id
            vals_line['journal_id'] = journal_id
            vals_line['general_account_id'] = general_account_id

            new_line_plan_id = line_plan_obj.create(
                cr, uid, vals=vals_line, context=context
            )

            vals['analytic_line_plan'] = new_line_plan_id

        order_line = super(purchase_order_line, self).create(
            cr, uid, vals, *args, **kwargs
        )

        return order_line

    def write(self, cr, uid, ids, vals, context=None):
        if context is None:
            context = {}

        purchase_order_obj = self.pool.get('purchase.order')
        line_plan_obj = self.pool.get('account.analytic.line.plan')
        plan_version_obj = self.pool.get('account.analytic.plan.version')
        plan_journal_obj = self.pool.get('account.analytic.plan.journal')
        product_obj = self.pool.get('product.product')
        currency_obj = self.pool.get('res.currency')

        vals_line = {}

        if isinstance(ids, (long, int)):
            ids = [ids]

        version_id = plan_version_obj.search(
            cr, uid, [('default_committed', '=', True)], context=context
        )[0]
        if not version_id:
            raise osv.except_osv(
                _('Error!'),
                _(
                    'Please define an analytic planning version '
                    'as default for committed costs.'
                )
            )

        j_ids = plan_journal_obj.search(
            cr, uid, [('type', '=', 'purchase')]
        )
        journal_id = j_ids and j_ids[0] or False
        if not journal_id:
            raise osv.except_osv(
                _('Error!'),
                _('Please define an analytic planning journal'
                  'for purchases.'
                  )
            )

        for po_line in self.browse(cr, uid, ids, context=context):

            order_id = po_line.order_id and po_line.order_id.id
            order = purchase_order_obj.browse(
                cr, uid, order_id, context=context
            )

            if 'state' in vals:
                line_state = vals['state']
            else:
                line_state = po_line.state

            if 'price_subtotal' in vals:
                price_subtotal = vals['price_subtotal']
            else:
                price_subtotal = po_line.price_subtotal

            if 'product_qty' in vals:
                product_qty = vals['product_qty']
            else:
                product_qty = po_line.product_qty

            if 'name' in vals:
                vals_line['name'] = vals['name']
            else:
                vals_line['name'] = po_line.name

            if 'date_planned' in vals:
                vals_line['date'] = vals['date_planned']
            else:
                vals_line['date'] = po_line.date_planned

            if 'account_analytic_id' in vals:
                vals_line['account_id'] = vals['account_analytic_id']
            else:
                vals_line['account_id'] = (
                    po_line.account_analytic_id and
                    po_line.account_analytic_id.id
                )

            vals_line['company_id'] = (
                order.company_id and
                order.company_id.id or
                False
            )

            if 'product_uom' in vals:
                vals_line['product_uom_id'] = vals['product_uom']
            else:
                vals_line['product_uom_id'] = (
                    po_line.product_uom and
                    po_line.product_uom.id
                )

            if 'product_id' in vals:
                vals_line['product_id'] = vals['product_id']
            else:
                vals_line['product_id'] = (
                    po_line.product_id and
                    po_line.product_id.id or
                    False
                )

            general_account_id = False
            if vals_line['product_id']:
                prod = product_obj.browse(
                    cr, uid,
                    vals_line['product_id'],
                    context=context
                )

                pptidx = prod.product_tmpl_id
                pcatecpx = prod.categ_id.property_account_expense_categ

                general_account_id = pptidx.property_account_expense.id
                if not general_account_id:
                    general_account_id = pcatecpx.id
                if not general_account_id:
                    raise osv.except_osv(
                        _('Error !'),
                        _('There is no expense account defined '
                          'for this product: "%s" (id:%d)')
                        % (prod.name, prod.id,))

            vals_line['general_account_id'] = general_account_id

            if order.currency_id.id != order.company_id.currency_id.id:

                amount_company_currency = currency_obj.compute(
                    cr,
                    uid,
                    order.currency_id.id,
                    order.company_id.currency_id.id,
                    price_subtotal,
                    context=context
                )
            else:
                amount_company_currency = price_subtotal

            if line_state in ('confirmed', 'done'):
                vals_line['amount'] = -1 * amount_company_currency
                vals_line['unit_amount'] = product_qty
            else:
                vals_line['amount'] = 0
                vals_line['unit_amount'] = 0

            vals_line['version_id'] = version_id
            vals_line['journal_id'] = journal_id

            if po_line.analytic_line_plan:
                if vals_line['account_id']:
                    line_plan_obj.write(
                        cr, uid,
                        [po_line.analytic_line_plan.id],
                        vals_line,
                        context
                    )
                else:
                    line_plan_obj.unlink(
                        cr, uid,
                        [po_line.analytic_line_plan.id],
                        context
                    )
            else:
                if vals_line['account_id']:
                    new_ana_line_plan = line_plan_obj.create(
                        cr, uid, vals_line, context=context
                    )
                    vals['analytic_line_plan'] = new_ana_line_plan

        return super(purchase_order_line, self).write(
            cr, uid, ids, vals, context=context
        )

    def unlink(self, cr, uid, ids, context=None):
        line_plan_obj = self.pool.get('account.analytic.line.plan')
        ana_line_plan_ids = []
        for order_line in self.browse(cr, uid, ids, context=context):
            if order_line.analytic_line_plan:
                ana_line_plan_ids.append(order_line.analytic_line_plan.id)
        res = super(purchase_order_line, self).unlink(
            cr, uid, ids, context=context
        )
        line_plan_obj.unlink(cr, uid, ana_line_plan_ids, context=context)
        return res

purchase_order_line()
