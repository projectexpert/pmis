# -*- coding: utf-8 -*-
#    Copyright 2017 Matmoz d.o.o. & Luxim d.o.o. (Matjaž Mozetič)
#    Copyright 2015 Eficent (Jordi Ballester Alomar)
#    License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

import openerp.addons.decimal_precision as dp
from openerp.osv import fields, orm


class AccountAnalyticAccount(orm.Model):
    _inherit = 'account.analytic.account'

    def _compute_level_tree_plan(
            self, cr, uid, ids, child_ids, res, field_names, context=None
    ):
        currency_obj = self.pool.get('res.currency')
        recres = {}

        def recursive_computation(account):
            result2 = res[account.id].copy()
            for son in account.child_ids:
                result = recursive_computation(son)
                for field in field_names:
                    if (account.currency_id.id != son.currency_id.id) \
                            and (field != 'quantity_plan'):
                        result[field] = currency_obj.compute(
                            cr, uid, son.currency_id.id,
                            account.currency_id.id, result[field],
                            context=context)
                    result2[field] += result[field]
            return result2

        for account in self.browse(cr, uid, ids, context=context):
            if account.id not in child_ids:
                continue
            recres[account.id] = recursive_computation(account)
        return recres

    def _compute_debit_credit_bal_qtty_plan(
            self, cr, uid, ids, fields, arg, context=None):
        res = {}
        if context is None:
            context = {}
        child_ids = tuple(self.search(
            cr, uid, [('parent_id', 'child_of', ids)])
        )
        for i in child_ids:
            res[i] = {}
            for n in fields:
                res[i][n] = 0.0

        if not child_ids:
            return res

        for ac_id in child_ids:
            res[ac_id] = {'debit_plan': 0,
                          'credit_plan': 0,
                          'balance_plan': 0,
                          'quantity_plan': 0}

        where_date = ''
        where_clause_args = [tuple(child_ids)]
        if context.get('from_date', False):
            where_date += " AND l.date >= %s"
            where_clause_args += [context['from_date']]
        if context.get('to_date', False):
            where_date += " AND l.date <= %s"
            where_clause_args += [context['to_date']]
        cr.execute("""
              SELECT a.id,
                     sum(
                         CASE WHEN l.amount > 0
                         THEN l.amount
                         ELSE 0.0
                         END
                          ) as debit_plan,
                     sum(
                         CASE WHEN l.amount < 0
                         THEN -l.amount
                         ELSE 0.0
                         END
                          ) as credit_plan,
                     COALESCE(SUM(l.amount),0) AS balance_plan,
                     COALESCE(SUM(l.unit_amount),0) AS quantity_plan
              FROM account_analytic_account a
                  LEFT JOIN account_analytic_line_plan l ON
                  (a.id = l.account_id)
              WHERE a.id IN %s
              AND a.active_analytic_planning_version = l.version_id
              """ + where_date + """             
              GROUP BY a.id""", where_clause_args)

        for row in cr.dictfetchall():
            res[row['id']] = {}
            for field in fields:
                res[row['id']][field] = row[field]
        return self._compute_level_tree_plan(
            cr, uid, ids, child_ids, res, fields, context
        )

    _columns = {

        'balance_plan': fields.function(
            _compute_debit_credit_bal_qtty_plan, method=True, type='float',
            string='Planned Balance', multi='debit_credit_bal_qtty_plan',
            digits_compute=dp.get_precision('Account')
        ),
        'debit_plan': fields.function(
            _compute_debit_credit_bal_qtty_plan, method=True, type='float',
            string='Planned Debit', multi='debit_credit_bal_qtty_plan',
            digits_compute=dp.get_precision('Account')
        ),
        'credit_plan': fields.function(
            _compute_debit_credit_bal_qtty_plan, method=True, type='float',
            string='Planned Credit', multi='debit_credit_bal_qtty_plan',
            digits_compute=dp.get_precision('Account')
        ),
        'quantity_plan': fields.function(
            _compute_debit_credit_bal_qtty_plan, method=True, type='float',
            string='Quantity Debit', multi='debit_credit_bal_qtty_plan',
            digits_compute=dp.get_precision('Account')
        ),
    }
