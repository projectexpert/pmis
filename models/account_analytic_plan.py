# -*- coding: utf-8 -*-
# Copyright 2015 Eficent Business and IT Consulting Services S.L.
# (Jordi Ballester Alomar)
# Copyright 2016 Matmoz d.o.o.
# (Matjaž Mozetič)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class AccountAnalyticLinePlan(models.Model):
    _name = 'account.analytic.line.plan'
    _description = 'Analytic Line'
    _order = 'date desc, id desc'

    @api.model
    def _default_user(self):
        return self.env.context.get('user_id', self.env.user.id)

    name = fields.Char(
        'Description',
        required=True
    )
    date = fields.Date(
        'Date',
        required=True,
        index=True,
        default=fields.Date.context_today
    )
    amount = fields.Float(
        'Amount',
        required=True,
        default=0.0
    )
    unit_amount = fields.Float(
        'Quantity',
        default=0.0
    )
    amount_currency = fields.Float(
        'Amount Currency',
        help="The amount expressed in an optional other currency."
    )
    account_id = fields.Many2one(
        'account.analytic.account',
        'Analytic Account',
        required=True,
        ondelete='restrict',
        index=True
    )
    partner_id = fields.Many2one(
        'res.partner',
        string='Partner'
    )
    user_id = fields.Many2one(
        'res.users',
        string='User',
        default=_default_user
    )
    company_id = fields.Many2one(
        related='account_id.company_id',
        string='Company',
        store=True,
        readonly=True
    )
    currency_id = fields.Many2one(
        related="company_id.currency_id",
        string="Currency",
        readonly=True
    )
    product_uom_id = fields.Many2one(
        'product.uom',
        'UoM'
    )
    product_id = fields.Many2one(
        'product.product',
        'Product'
    )
    general_account_id = fields.Many2one(
        'account.account',
        'General Account',
        required=True,
        ondelete='restrict'
    )
    journal_id = fields.Many2one(
        'account.analytic.plan.journal',
        'Planning Analytic Journal',
        required=True,
        ondelete='restrict',
        index=True,
        default=lambda self:
        self._context['journal_id'] if
        self._context and 'journal_id' in
        self._context else None
    )
    code = fields.Char(
        'Code'
    )
    ref = fields.Char(
        'Ref.'
    )
    notes = fields.Text(
        'Notes'
    )
    version_id = fields.Many2one(
        'account.analytic.plan.version',
        'Planning Version',
        required=True,
        ondelete='cascade',
        default=lambda s:
        s.env[
            'account.analytic.plan.version'
        ].search(
            [('default_plan', '=', True)], limit=1
        )
    )

    @api.onchange('amount_currency', 'currency_id')
    def on_change_amount_currency(self):
        company = self.company_id
        company_currency = company.currency_id
        currency = self.currency_id
        if self.amount_currency:
            amount_company_currency = currency.compute(
                self.amount_currency,
                company_currency
            )
        else:
            amount_company_currency = 0.0
        self.amount = amount_company_currency
        return {}

    @api.onchange('unit_amount', 'product_uom_id')
    def on_change_unit_amount(self):
        analytic_journal_obj = self.env['account.analytic.plan.journal']
        product_price_type_obj = self.env['product.pricelist.item']

        prod = False
        journal = self.journal_id if self.journal_id else analytic_journal_obj
        if self.product_id:
            prod = self.product_id
        if not self.journal_id:
            j = analytic_journal_obj.search([('type', '=', 'purchase')])
            journal = j[0] if j and j[0] else False
        if not self.journal_id or not self.product_id:
            return {}
        if journal.type != 'sale' and prod:
            a = prod.product_tmpl_id.property_account_income_id.id
            if not a:
                a = prod.categ_id.property_account_income_categ_id.id
            if not a:
                raise UserError(
                    _('There is no expense account defined '
                      'for this product: "%s" (id:%d)')
                    % (prod.name, prod.id,)
                )
        else:
            a = prod.product_tmpl_id.property_account_income_id.id
            if not a:
                a = prod.categ_id.property_account_income_categ_id.id
            if not a:
                raise UserError(
                    _('There is no income account defined '
                      'for this product: "%s" (id:%d)')
                    % (prod.name, self.product_id,)
                )
        flag = False
        # Compute based on pricetype
        product_price_type = product_price_type_obj.search([])
        pricetype = product_price_type[0]
        if self.journal_id:
            if journal.type == 'sale':
                product_price_type = product_price_type_obj.\
                    search([('base', '=', 'list_price')])
                if product_price_type:
                    pricetype = product_price_type[0]
        # Take the company currency as the reference one
        if pricetype.base == 'list_price':
            flag = True
        cr, uid, context = self.env.args
        ctx = dict(context.copy())
        if self.product_uom_id:
            # price_get() will respect a 'uom' in its context, in order
            # to return a default price for those units
            ctx['uom'] = self.product_uom_id.id
        amount_unit = prod.with_context(ctx).price_get(
            pricetype.base)[prod.id]
#        self.env.args = cr, uid, misc.frozendict(context)
        prec = self.env['decimal.precision'].precision_get('Account')
        amount = amount_unit * self.unit_amount or 1.0
        result = round(amount, prec)
        if not flag:
            if journal.type != 'sale':
                result *= -1
        self.amount_currency = result
        self.general_account_id = a
        return {}

    @api.onchange('product_id')
    def on_change_product_id(self):
        self.on_change_unit_amount()
        prod = self.product_id
        self.name = prod.name
        if prod.uom_id:
            self.product_uom_id = prod.uom_id.id
        return {}
