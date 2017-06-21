# -*- coding: utf-8 -*-
# © 2015 Eficent Business and IT Consulting Services S.L.
# (Jordi Ballester Alomar)
#
# © 2016 Matmoz d.o.o.
# (Matjaž Mozetič)
#
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models


class AccountAnalyticAccount(models.Model):

    _inherit = 'account.analytic.account'

    @api.model
    def default_version(self):
        plan_versions = self.env[
            'account.analytic.plan.version'
        ].search(
            [('default_plan', '=', True)]
        )
        return plan_versions

    @api.multi
    def _compute_debit_credit_bal_qtty_plan(self):
        analytic_line_obj = self.env['account.analytic.line.plan']
        domain = [('account_id', 'in', self.mapped('id'))]
        if self._context.get('from_date', False):
            domain.append(('date', '>=', self._context['from_date']))
        if self._context.get('to_date', False):
            domain.append(('date', '<=', self._context['to_date']))

        account_amounts = analytic_line_obj.search_read(
            domain, ['account_id', 'amount']
        )
        account_ids = set(
            [line['account_id'][0] for line in account_amounts]
        )
        data_debit_plan = {account_id: 0.0 for account_id in account_ids}
        data_credit_plan = {account_id: 0.0 for account_id in account_ids}
        for account_amount in account_amounts:
            if account_amount['amount'] < 0.0:
                data_debit_plan[
                    account_amount['account_id'][0]
                ] += account_amount['amount']
            else:
                data_credit_plan[
                    account_amount['account_id'][0]
                ] += account_amount['amount']

        for account in self:
            account.debit_plan = abs(data_debit_plan.get(account.id, 0.0))
            account.credit_plan = data_credit_plan.get(account.id, 0.0)
            account.balance_plan = account.credit_plan - account.debit_plan

    plan_line_ids = fields.One2many(
        'account.analytic.line.plan', 'account_id', string="Analytic Entries")

    company_id = fields.Many2one(
        'res.company', string='Company', required=True,
        default=lambda self: self.env.user.company_id
    )

    balance_plan = fields.Float(
        compute='_compute_debit_credit_bal_qtty_plan',
        string='Planned Balance'
    )
    debit_plan = fields.Float(
        compute='_compute_debit_credit_bal_qtty_plan',
        string='Planned Debit'
    )
    credit_plan = fields.Float(
        compute='_compute_debit_credit_bal_qtty_plan',
        string='Planned Credit'
    )

    currency_id = fields.Many2one(
        related="company_id.currency_id",
        string="Currency", readonly=True
    )

    active_analytic_planning_version = fields.Many2one(
        'account.analytic.plan.version',
        'Active planning Version',
        required=True,
        default=default_version
    )


class AccountAnalyticLine(models.Model):
    _name = 'account.analytic.line.plan'
    _description = 'Analytic Line'
    _order = 'date desc, id desc'

    @api.model
    def _default_user(self):
        return self.env.context.get('user_id', self.env.user.id)

    name = fields.Char(
        'Description', required=True
    )
    date = fields.Date(
        'Date', required=True, index=True,
        default=fields.Date.context_today
    )
    amount = fields.Float(
        'Amount', required=True, default=0.0
    )
    unit_amount = fields.Float(
        'Quantity', default=0.0
    )
    # amount_currency = fields.Float(
    #     'Amount Currency',
    #     help="The amount expressed in an "
    #          "optional other currency."
    # )
    account_id = fields.Many2one(
        'account.analytic.account',
        'Analytic Account', required=True,
        ondelete='restrict', index=True
    )
    # partner_id = fields.Many2one(
    #     'res.partner', string='Partner'
    # )
    user_id = fields.Many2one(
        'res.users', string='User',
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
        'product.uom', 'UoM'
    )
    product_id = fields.Many2one(
        'product.product', 'Product'
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
        select=True,
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
            [('default_plan', '=', True)]
        )
    )

    # @api.onchange('amount_currency', 'currency_id')
    # def on_change_amount_currency(self):
    #     company = self.company_id
    #     company_currency = company.currency_id
    #     currency = self.currency_id
    #     if self.amount_currency:
    #         amount_company_currency = currency.compute(
    #             self.amount_currency,
    #             company_currency
    #         )
    #     else:
    #         amount_company_currency = 0.0
    #     self.amount = amount_company_currency
    #     return {}

    @api.onchange('unit_amount', 'product_uom_id')
    def on_change_unit_amount(self):
        analytic_journal_obj = self.env['account.analytic.plan.journal']
        product_price_type_obj = self.env['product.price.type']

        prod = False
        journal = self.journal_id if self.journal_id else journal
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
        amount = amount_unit * self.unit_amount or 1.0
        result = round(amount, prec)
        if not flag:
            if journal.type != 'sale':
                result *= -1
        # self.amount_currency = result
        self.general_account_id = a
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
