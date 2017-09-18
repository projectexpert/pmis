# -*- coding: utf-8 -*-
# Copyright 2015 Eficent - Jordi Ballester Alomar
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class AnalyticAccountOpen(models.TransientModel):
    _name = 'analytic.account.open'
    _description = 'Open single analytic account'

    analytic_account_id = fields.Many2one(
        'account.analytic.account',
        'Analytic Account',
        required=True
    )
    include_child = fields.Boolean(
        'Include child accounts',
        default=True
    )

    @api.model
    def _get_child_analytic_accounts(self, curr_id):
        result = {}
        result[curr_id] = True
        # Now add the children
        self.env.cr.execute('''
        WITH RECURSIVE children AS (
        SELECT parent_id, id
        FROM account_analytic_account
        WHERE parent_id = %s
        UNION ALL
        SELECT a.parent_id, a.id
        FROM account_analytic_account a
        JOIN children b ON(a.parent_id = b.id)
        )
        SELECT * FROM children order by parent_id
        ''', (curr_id,))
        res = self.env.cr.fetchall()
        for x, y in res:
            result[y] = True
        return result

    @api.multi
    def analytic_account_open_window(self):
        self.ensure_one()
        act_window_id = self.env.ref(
            'analytic.action_account_analytic_account_form')
        result = act_window_id.read()[0]
        acc_id = self.analytic_account_id.id
        acc_ids = []
        if self.include_child:
            acc_ids = self._get_child_analytic_accounts(acc_id)
        else:
            acc_ids.append(acc_id)
        result['domain'] = "[('id','in', ["+','.join(map(str, acc_ids))+"])]"
        return result
