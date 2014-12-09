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
import openerp.addons.decimal_precision as dp
from openerp.osv import fields, osv


class account_analytic_account(osv.osv):
    
    _inherit = 'account.analytic.account'

    def _get_active_analytic_planning_version(self, cr, uid, ids, context=None):

        planning_versions = self.pool.get('account.analytic.plan.version').search(cr, uid,
                                                              [('default_plan', '=', True)],
                                                              context=None),
        for planning_version in planning_versions:
            if planning_version:
                return planning_version[0]

        return False

    def _compute_level_tree_plan(self, cr, uid, ids, child_ids, res, field_names, context=None):
        currency_obj = self.pool.get('res.currency')
        recres = {}

        def recursive_computation(account):
            result2 = res[account.id].copy()
            for son in account.child_ids:
                result = recursive_computation(son)
                for field in field_names:
                    if (account.currency_id.id != son.currency_id.id) and (field != 'quantity_plan'):
                        result[field] = currency_obj.compute(cr, uid,
                                                             son.currency_id.id,
                                                             account.currency_id.id,
                                                             result[field],
                                                             context=context)
                    result2[field] += result[field]
            return result2
        for account in self.browse(cr, uid, ids, context=context):
            if account.id not in child_ids:
                continue
            recres[account.id] = recursive_computation(account)
        return recres

    def _debit_credit_bal_qtty_plan(self, cr, uid, ids, fields, arg, context=None):
        res = {}
        if context is None:
            context = {}
        child_ids = tuple(self.search(cr, uid, [('parent_id', 'child_of', ids)]))
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
                  LEFT JOIN account_analytic_line_plan l ON (a.id = l.account_id)
              WHERE a.id IN %s
              AND a.active_analytic_planning_version = l.version_id
              """ + where_date + """             
              GROUP BY a.id""", where_clause_args)
        
        for row in cr.dictfetchall():
            res[row['id']] = {}
            for field in fields:
                res[row['id']][field] = row[field]
        return self._compute_level_tree_plan(cr, uid, ids, child_ids, res, fields, context)

    _columns = {   

        'balance_plan': fields.function(_debit_credit_bal_qtty_plan,
                                        method=True,
                                        type='float',
                                        string='Planned Balance',
                                        multi='debit_credit_bal_qtty_plan',
                                        digits_compute=dp.get_precision('Account')),
        'debit_plan': fields.function(_debit_credit_bal_qtty_plan,
                                      method=True,
                                      type='float',
                                      string='Planned Debit',
                                      multi='debit_credit_bal_qtty_plan',
                                      digits_compute=dp.get_precision('Account')),
        'credit_plan': fields.function(_debit_credit_bal_qtty_plan,
                                       method=True,
                                       type='float',
                                       string='Planned Credit',
                                       multi='debit_credit_bal_qtty_plan',
                                       digits_compute=dp.get_precision('Account')),
        'quantity_plan': fields.function(_debit_credit_bal_qtty_plan,
                                         method=True,
                                         type='float',
                                         string='Quantity Debit',
                                         multi='debit_credit_bal_qtty_plan',
                                         digits_compute=dp.get_precision('Account')),
        'plan_line_ids': fields.one2many('account.analytic.line.plan',
                                         'account_id',
                                         'Analytic Entries'),

        'active_analytic_planning_version': fields.many2one('account.analytic.plan.version',
                                                            'Active planning Version', required=True),
    }

    _defaults = {

        'active_analytic_planning_version': _get_active_analytic_planning_version
    }

    def copy(self, cr, uid, id, default=None, context=None):
        if default is None:
            default = {}        
        default['plan_line_ids'] = []        
        return super(account_analytic_account, self).copy(cr, uid, id, default, context=context)
    
                
account_analytic_account()