# -*- coding: utf-8 -*-
#    Copyright 2017 Matmoz d.o.o. & Luxim d.o.o. (Matjaž Mozetič)
#    Copyright 2015 Eficent (Jordi Ballester Alomar)
#    License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models


class AccountAnalyticAccount(models.Model):
    _inherit = 'account.analytic.account'

    @api.v8
    @api.model
    def default_version(self):
        plan_versions = self.env['account.analytic.plan.version'].search(
            [('default_plan', '=', True)], limit=1
        )
        for plan_version in plan_versions:
            if plan_version:
                res['active_analytic_planning_version'] = plan_version[0]
                return res
        return plan_versions

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
    # balance_plan = fields.Float(
    #     compute='_compute_debit_credit_bal_qtty_plan',
    #     string='Planned Balance'
    # )
    # debit_plan = fields.Float(
    #     compute='_compute_debit_credit_bal_qtty_plan',
    #     string='Planned Debit'
    # )
    # credit_plan = fields.Float(
    #     compute='_compute_debit_credit_bal_qtty_plan',
    #     string='Planned Credit'
    # )
    # currency_id = fields.Many2one(
    #     related="company_id.currency_id",
    #     string="Currency",
    #     readonly=True
    # )
    active_analytic_planning_version = fields.Many2one(
        'account.analytic.plan.version',
        'Active planning Version',
        required=True,
        default=default_version
    )

    @api.multi
    def action_openplancostlist(self):
        """
        :return dict: dictionary value for created view
        """
        account = self[0]
        res = self.env['ir.actions.act_window'].for_xml_id(
            'analytic_plan',
            'action_account_analytic_plan_journal_open_form'
        )
        plan_obj = self.env['account.analytic.line.plan']
        acc_ids = account.get_child_accounts()
        line = plan_obj.search(
            [
                ('account_id', 'in', acc_ids.keys()),
                ('version_id', '=', account.active_analytic_planning_version.id)
            ]
        )
        res['domain'] = "[('id', 'in', [" + ','.join(
            map(str, line.ids)) + "])]"
        res['nodestroy'] = False
        return res
