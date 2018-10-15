# -*- coding: utf-8 -*-
# Copyright 2015 Eficent Business and IT Consulting Services S.L.
# (Jordi Ballester Alomar)
# Copyright 2016 Matmoz d.o.o. and 2018 Luxim d.o.o.s
# (Matjaž Mozetič)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models, _
from odoo.exceptions import UserError


# noinspection PyTypeChecker
class AccountAnalyticLinePlan(models.Model):
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
        store=True,
        compute='_compute_total_amount'
    )
    unit_amount = fields.Float(
        string='Quantity',
        default=0.0
    )
    unit_price = fields.Float(
        string='Unit Price'
    )
    amount_currency = fields.Float(
        string='Amount Currency',
        help="The amount expressed in an optional other currency."
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
        comodel_name='product.uom',
        string='UoM'
    )
    product_id = fields.Many2one(
        comodel_name='product.product',
        string='Product'
    )
    general_account_id = fields.Many2one(
        comodel_name='account.account',
        string='General Account',
        required=True,
        ondelete='restrict'
    )
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
            [('default_plan', '=', True)], limit=1
        )
    )

    @api.multi
    def _set_unit_price(self):
        analytic_journal_obj = self.env['account.analytic.plan.journal']

        journal = self.journal_id if self.journal_id else analytic_journal_obj
        if journal.type != 'sale':
            for line in self:
                pricelist_id = line._get_pricelist()
                line.unit_price = line.product_id.standard_price
                if pricelist_id and line.partner_id \
                        and line.product_uom_id:
                    product = line.product_id.with_context(
                        lang=line.partner_id.lang,
                        partner=line.partner_id.id,
                        unit_amount=line.unit_amount,
                        pricelist=pricelist_id.id,
                        product_uom=line.product_uom_id.id,
                    )
                    line.unit_price = product.price

        else:
            for line in self:
                pricelist_id = line._get_pricelist()
                line.unit_price = line.product_id.lst_price
                if pricelist_id and line.partner_id \
                        and line.product_uom_id:
                    product = line.product_id.with_context(
                        lang=line.partner_id.lang,
                        partner=line.partner_id.id,
                        unit_amount=line.unit_amount,
                        pricelist=pricelist_id.id,
                        product_uom=line.product_uom_id.id,
                    )
                    line.unit_price = product.price

    @api.multi
    @api.depends('unit_price', 'unit_amount')
    def _compute_total_amount(self):
        analytic_journal_obj = self.env['account.analytic.plan.journal']

        journal = self.journal_id if self.journal_id else analytic_journal_obj
        if journal.type != 'sale':
            for line in self:
                line.amount = -1 * line.unit_price * line.unit_amount
        else:
            for line in self:
                line.amount = line.unit_price * line.unit_amount

    @api.multi
    def _get_pricelist(self):
        self.ensure_one()
        if self.partner_id:
            return (
                self.partner_id.property_product_pricelist)
        else:
            return False

    @api.multi
    @api.onchange('product_id')
    def product_id_change(self):
        self.ensure_one()
        analytic_journal_obj = self.env['account.analytic.plan.journal']

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
            a = prod.product_tmpl_id.property_account_expense_id.id
            if not a:
                a = prod.categ_id.property_account_expense_categ_id.id
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
        if prod.uom_id:
            self.product_uom_id = prod.uom_id.id

        self._set_unit_price()
        self.general_account_id = a
        self.name = prod.name

    @api.multi
    @api.onchange('product_uom_id', 'unit_amount')
    def product_uom_change(self):
        self.ensure_one()
        analytic_journal_obj = self.env['account.analytic.plan.journal']

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
            a = prod.product_tmpl_id.property_account_expense_id.id
            if not a:
                a = prod.categ_id.property_account_expense_categ_id.id
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
        self._set_unit_price()
        self.general_account_id = a

    @api.onchange('journal_id')
    def journal_change(self):
        analytic_journal_obj = self.env['account.analytic.plan.journal']
        prod = False
        journal = self.journal_id if self.journal_id else self
        if not self.journal_id:
            j = analytic_journal_obj.search(
                [('type', '=', 'purchase')]
            )
            journal = j[0] if j and j[0] else False
        if not self.journal_id or not self.product_id:
            return {}
        if self.product_id:
            prod = self.product_id

        if journal.type != 'sale' and prod:
            a = prod.product_tmpl_id.property_account_expense_id.id
            if not a:
                a = prod.categ_id.property_account_expense_categ_id.id
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

        self._set_unit_price()
        self._compute_total_amount()
        self.general_account_id = a
