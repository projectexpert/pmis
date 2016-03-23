# -*- coding: utf-8 -*-
# © 2015 Eficent - Jordi Ballester Alomar
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openerp import models, fields


class AnalyticAccountOpen(models.TransientModel):
    _name = 'analytic.account.open'
    _description = 'Open single analytic account'

    analytic_account_id = fields.Many2one(
        'account.analytic.account',
        'Analytic Account',
        required=True
    )
    include_child = fields.Boolean(
        'Include child accounts', default=True
    )

    def _get_child_analytic_accounts(self, cr, uid, curr_id, context=None):

        result = {}
        result[curr_id] = True
        # Now add the children
        cr.execute('''
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
        res = cr.fetchall()
        for x, y in res:
            result[y] = True
        return result

    def analytic_account_open_window(self, cr, uid, ids, context=None):
        mod_obj = self.pool['ir.model.data']
        act_obj = self.pool['ir.actions.act_window']

        if context is None:
            context = {}
        act_window = mod_obj.get_object_reference(
                cr, uid, 'account',
                'action_account_analytic_account_form')
        act_window_id = act_window and act_window[1] or False
        result = act_obj.read(cr, uid, [act_window_id], context=context)[0]
        data = self.read(cr, uid, ids, [])[0]
        acc_id = data['analytic_account_id'][0]
        acc_ids = []

        if data['include_child']:
            acc_ids = self._get_child_analytic_accounts(
                cr, uid, acc_id, context=context)
        else:
            acc_ids.append(acc_id)

        result['domain'] = "[('id','in', ["+','.join(map(str, acc_ids))+"])]"

        return result
