# -*- coding: utf-8 -*-
#    Copyright 2017 Matmoz d.o.o. & Luxim d.o.o. (Matjaž Mozetič)
#    Copyright 2015 Eficent (Jordi Ballester Alomar)
#    License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models
from openerp.tools.translate import _
from openerp.exceptions import Warning as UserError
from openerp.tools import misc


class AccountAnalyticLine(models.Model):
    _name = 'account.analytic.line.plan'
    _description = 'Analytic Line'
    _order = 'date desc, id desc'

    @api.model
    def _default_user(self):
        return self.env.context.get('user_id', self.env.user.id)

    name = fields.Char(
        string='Description',
        required=True
    )
    date = fields.Date(
        string='Date',
        required=True,
        index=True,
        default=fields.Date.context_today
    )
    amount = fields.Float(
        string='Amount',
        required=True,
        default=0.0,
    )
    unit_amount = fields.Float(
        string='Quantity',
        default=0.0,
        oldname='quantity'
    )
    account_id = fields.Many2one(
        comodel_name='account.analytic.account',
        string='Analytic Account',
        required=True,
        ondelete='restrict',
        index=True
    )
    partner_id = fields.Many2one(
        comodel_name='res.partner',
        string='Partner'
    )
    user_id = fields.Many2one(
        comodel_name='res.users',
        string='User',
        default=_default_user
    )
    company_id = fields.Many2one(
        related='account_id.company_id',
        string='Company', store=True,
        readonly=True
    )
    currency_id = fields.Many2one(
        related="company_id.currency_id",
        string="Currency", readonly=True
    )
    product_uom_id = fields.Many2one(
        comodel_name='product.uom',
        string='UoM'
    )
    product_id = fields.Many2one(
        comodel_name='product.product',
        string='Product'
    )
    # general_account_id = fields.Many2one(
    #     'account.account',
    #     'General Account',
    #     # required=True,
    #     # ondelete='restrict'
    # )
    journal_id = fields.Many2one(
        comodel_name='account.analytic.plan.journal',
        string='Planning Journal',
        required=True,
        ondelete='restrict',
        index=True,
        default=lambda self:
        self._context['journal_id'] if
        self._context and 'journal_id' in
        self._context else None
    )
    code = fields.Char(
        string='Code'
    )
    ref = fields.Char(
        string='Ref.'
    )
    notes = fields.Text(
        string='Notes'
    )
    version_id = fields.Many2one(
        comodel_name='account.analytic.plan.version',
        string='Planning Version',
        required=True,
        ondelete='cascade',
        default=lambda s:
        s.env[
            'account.analytic.plan.version'
        ].search(
            [('default_plan', '=', True)]
        )
    )

    @api.onchange('unit_amount', 'product_uom_id', 'journal_id')
    def on_change_unit_amount(self):
        analytic_journal_obj = self.env['account.analytic.plan.journal']
        product_price_type_obj = self.env['product.price.type']

        prod = False
        journal = self.journal_id if self.journal_id else self
        if self.product_id:
            prod = self.product_id
        if not self.journal_id:
            j = analytic_journal_obj.search(
                [('type', '=', 'purchase')]
            )
            journal = j[0] if j and j[0] else False
        if not self.journal_id or not self.product_id:
            return {}
        if journal.type != 'sale' and prod:
            a = prod.product_tmpl_id.property_account_expense.id
            if not a:
                a = prod.categ_id.property_account_expense_categ.id
            if not a:
                raise UserError(
                    _(
                        'There is no expense account defined '
                        'for this product: "%s" (id:%d)'
                    ) % (prod.name, prod.id,)
                )
        else:
            a = prod.product_tmpl_id.property_account_income.id
            if not a:
                a = prod.categ_id.property_account_income_categ.id
            if not a:
                raise UserError(
                    _(
                        'There is no income account defined '
                        'for this product: "%s" (id:%d)'
                    ) % (prod.name, self.product_id,)
                )
        flag = False
        # Compute based on pricetype
        product_price_type = product_price_type_obj.search(
            [('field', '=', 'standard_price')]
        )
        pricetype = product_price_type[0]
        if self.journal_id:
            if journal.type == 'sale':
                product_price_type = product_price_type_obj.search(
                    [('field', '=', 'list_price')]
                )
                if product_price_type:
                    pricetype = product_price_type[0]
        # Take the company currency as the reference one
        if pricetype.field == 'list_price':
            flag = True
        cr, uid, context = self.env.args
        ctx = dict(context.copy())
        if self.product_uom_id:
            # price_get() will respect a 'uom' in its context, in order
            # to return a default price for those units
            ctx['uom'] = self.product_uom_id.id
        amount_unit = prod.with_context(ctx).price_get(
            pricetype.field)[prod.id]
        self.env.args = cr, uid, misc.frozendict(context)
        prec = self.env['decimal.precision'].precision_get('Account')
        self.amount = amount_unit * self.unit_amount or 1.0
        result = round(self.amount, prec)
        if not flag:
            if journal.type != 'sale':
                self.amount = -1 * amount_unit * self.unit_amount or -1.0
                result = round(self.amount, prec)
        # self.amount_currency = result
        # self.general_account_id = a
        # self.on_change_amount_currency()
        return {}

    @api.onchange('product_id')
    def on_change_product_id(self):
        self.on_change_unit_amount()
        prod = self.product_id
        self.name = prod.name
        if prod.uom_id:
            self.product_uom_id = prod.uom_id.id
        return {}
