# -*- coding: utf-8 -*-
# Copyright 2015 Eficent Business and IT Consulting Services S.L.
# (Jordi Ballester Alomar)
# Copyright 2016 Matmoz d.o.o.
# (Matjaž Mozetič)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class AccountAnalyticAccount(models.Model):

    _inherit = 'account.analytic.account'

    @api.model
    def default_version(self):
        plan_versions = self.env['account.analytic.plan.version'].\
            search([('default_plan', '=', True)], limit=1)
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
        'account.analytic.line.plan',
        'account_id',
        string="Analytic Entries"
    )
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        required=True,
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
        string="Currency",
        readonly=True
    )
    active_analytic_planning_version = fields.Many2one(
        'account.analytic.plan.version',
        'Active planning Version',
        required=True,
        default=default_version
    )
