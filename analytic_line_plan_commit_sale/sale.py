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
from datetime import date


class sale_order(osv.osv):

    _inherit = 'sale.order'

    def write(self, cr, uid, ids, data, context=None):
        if context is None:
            context = {}

        so_line_obj = self.pool.get('sale.order.line')
        line_plan_obj = self.pool.get('account.analytic.line.plan')

        for so in self.browse(cr, uid, ids, context=context):
            for order_line_id in so.order_line:
                for order_line in so_line_obj.browse(
                    cr, uid, [order_line_id.id], context=context
                ):
                    vals_line = {}
                    if order_line.analytic_line_plan:
                        if 'state' in data:
                            if data['state'] in ('confirmed', 'done'):
                                vals_line[
                                    'amount'
                                ] = order_line.price_subtotal
                                vals_line[
                                    'unit_amount'
                                ] = order_line.product_uom_qty
                            else:
                                vals_line['amount'] = 0
                                vals_line['unit_amount'] = 0
                        if 'company_id' in data:
                            vals_line['company_id'] = data['company_id']
                        if 'date_confirm' in data:
                            vals_line['date'] = data['date_confirm']

                        line_plan_obj.write(
                            cr, uid,
                            [order_line.analytic_line_plan.id],
                            vals_line,
                            context
                        )

        return super(sale_order, self).write(
            cr, uid, ids, data, context=context
        )

sale_order()


class sale_order_line(osv.osv):

    _inherit = 'sale.order.line'

    _columns = {
        'analytic_line_plan': fields.many2one(
            'account.analytic.line.plan',
            'Planning Analytic line'
        ),
    }

    def reset_analytic_line_plan(
        self, cr, uid, analytic_line_plan_id, order_state, context=None
    ):
        if context is None:
            context = {}
        line_plan_obj = self.pool.get('account.analytic.line.plan')

        vals_line = {}

        if order_state not in (
            'progress',
            'manual',
            'invoice_except',
            'done'
        ):
            vals_line['amount'] = 0
            vals_line['unit_amount'] = 0

        line_plan_obj.write(
            cr, uid, [analytic_line_plan_id], vals_line, context
        )

    def create(self, cr, uid, vals, *args, **kwargs):
        sale_order_obj = self.pool.get('sale.order')
        line_plan_obj = self.pool.get('account.analytic.line.plan')
        plan_version_obj = self.pool.get('account.analytic.plan.version')
        plan_journal_obj = self.pool.get('account.analytic.plan.journal')
        vals_line = {}
        new_line_plan_id = False
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

            j_ids = plan_journal_obj.search(cr, uid, [('type', '=', 'sale')])
            journal_id = j_ids and j_ids[0] or False
            if not journal_id:
                raise osv.except_osv(
                    _('Error!'),
                    _('Please define an analytic planning journal for sales.')
                )

            order = False
            if 'order_id' in vals:
                order = sale_order_obj.browse(
                    cr, uid,
                    vals['order_id'],
                    context=context
                )

            vals_line['name'] = vals['name']
            vals_line['date'] = order.date_confirm or date.today()
            vals_line['amount'] = 0
            vals_line['amount_currency'] = 0
            if order.currency_id:
                vals_line['currency_id'] = order.currency_id.id
            vals_line['unit_amount'] = 0
            vals_line['account_id'] = (
                order.project_id and
                order.project_id.id or
                False
            )
            vals_line['company_id'] = (
                order.company_id and
                order.company_id.id or
                False
            )
            vals_line['product_uom_id'] = vals['product_uos']
            vals_line['product_id'] = vals['product_id']
            vals_line['version_id'] = version_id
            vals_line['journal_id'] = journal_id

            new_line_plan_id = line_plan_obj.create(
                cr, uid,
                vals=vals_line,
                context=context
            )

            vals['analytic_line_plan'] = new_line_plan_id

        order_line = super(sale_order_line, self).create(
            cr, uid, vals, *args, **kwargs
        )
        if new_line_plan_id:
            vals_line['sale_line_id'] = order_line
            line_plan_obj.write(
                cr, uid,
                [new_line_plan_id],
                vals_line,
                context=context
            )

        return order_line

    def write(self, cr, uid, ids, data, context=None):
        if context is None:
            context = {}

        sale_order_obj = self.pool.get('sale.order')
        line_plan_obj = self.pool.get('account.analytic.line.plan')
        plan_version_obj = self.pool.get('account.analytic.plan.version')
        plan_journal_obj = self.pool.get('account.analytic.plan.journal')

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
                    'as default for committed revenues.'
                  )
            )

        j_ids = plan_journal_obj.search(cr, uid, [('type', '=', 'sale')])
        journal_id = j_ids and j_ids[0] or False
        if not journal_id:
            raise osv.except_osv(
                _('Error!'),
                _(
                    'Please define an analytic planning journal for sales.'
                )
            )

        for so_line in self.browse(cr, uid, ids, context=context):

            order_id = so_line.order_id and so_line.order_id.id
            order = sale_order_obj.browse(cr, uid, order_id, context=context)

            if 'state' in data:
                line_state = data['state']
            else:
                line_state = so_line.state

            if 'price_subtotal' in data:
                price_subtotal = data['price_subtotal']
            else:
                price_subtotal = so_line.price_subtotal

            if 'product_qty' in data:
                product_qty = data['product_qty']
            else:
                product_qty = so_line.product_uom_qty

            if 'name' in data:
                vals_line['name'] = data['name']
            else:
                vals_line['name'] = so_line.name

            vals_line['date'] = order.date_confirm or date.today()

            if line_state in ('confirmed', 'done'):
                vals_line['amount_currency'] = price_subtotal
                if order.currency_id:
                    vals_line['currency_id'] = order.currency_id.id

                currency_obj = self.pool.get('res.currency')
                company_obj = self.pool.get('res.company')

                if order.company_id:
                    company = company_obj.browse(
                        cr, uid, order.company_id.id, context=context
                    )
                    if order.currency_id and company.currency_id:
                        company_currency_id = company.currency_id.id
                        vals_line['amount'] = currency_obj.compute(
                            cr,
                            uid,
                            order.currency_id.id,
                            company_currency_id,
                            price_subtotal,
                            context=context
                        )
                vals_line['unit_amount'] = product_qty
            else:
                vals_line['amount'] = 0
                vals_line['amount_currency'] = 0
                vals_line['unit_amount'] = 0

            if 'account_analytic_id' in data:
                vals_line['account_id'] = data['account_analytic_id']
            else:
                vals_line['account_id'] = (
                    so_line.order_id and
                    so_line.order_id.project_id and
                    so_line.order_id.project_id.id
                )

            vals_line['company_id'] = (
                order.company_id and
                order.company_id.id or
                False
            )

            if 'product_uos' in data:
                vals_line['product_uom_id'] = data['product_uos']
            else:
                vals_line['product_uom_id'] = (
                    so_line.product_uom and
                    so_line.product_uom.id
                )

            if 'product_id' in data:
                vals_line['product_id'] = data['product_id']
            else:
                vals_line['product_id'] = (
                    so_line.product_id and
                    so_line.product_id.id
                )

            vals_line['version_id'] = version_id
            vals_line['journal_id'] = journal_id

            if so_line.analytic_line_plan:
                if vals_line['account_id']:
                    line_plan_obj.write(
                        cr, uid,
                        [so_line.analytic_line_plan.id],
                        vals_line,
                        context
                    )
                else:
                    line_plan_obj.unlink(
                        cr, uid,
                        [so_line.analytic_line_plan.id],
                        context
                    )
            else:
                if vals_line['account_id']:
                    new_ana_line_plan = line_plan_obj.create(
                        cr, uid,
                        vals_line,
                        context=context
                    )
                    data['analytic_line_plan'] = new_ana_line_plan

        return super(sale_order_line, self).write(
            cr, uid, ids, data, context=context
        )

    def unlink(self, cr, uid, ids, context=None):
        line_plan_obj = self.pool.get('account.analytic.line.plan')
        ana_line_plan_ids = []
        for order_line in self.browse(cr, uid, ids, context=context):
            if order_line.analytic_line_plan:
                ana_line_plan_ids.append(order_line.analytic_line_plan.id)
        res = super(sale_order_line, self).unlink(
            cr, uid, ids, context=context
        )
        line_plan_obj.unlink(cr, uid, ana_line_plan_ids, context=context)
        return res


sale_order_line()
