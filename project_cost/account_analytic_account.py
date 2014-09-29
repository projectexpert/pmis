# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2011 Eficent (<http://www.eficent.com/>)
#              Jordi Ballester Alomar <jordi.ballester@eficent.com>
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
    
    def _compute_level_tree_plan(self, cr, uid, ids, child_ids, res, field_names, context=None):
        def recursive_computation(account_id, res, repeated_account_ids=[]):
            currency_obj = self.pool.get('res.currency')
            account = self.browse(cr, uid, account_id)
            for son in account.child_ids:
                if son.id in repeated_account_ids:
                    continue
                res = recursive_computation(son.id, res)
                repeated_account_ids.append(son.id)
                for field in field_names:
                    if account.currency_id.id == son.currency_id.id or field=='quantity_plan':
                        res[account.id][field] += res[son.id][field]
                    else:
                        res[account.id][field] += currency_obj.compute(cr, uid, son.currency_id.id, account.currency_id.id, res[son.id][field], context=context)
            return res
        for account in self.browse(cr, uid, ids, context=context):
            if account.id not in child_ids:
                continue
            res = recursive_computation(account.id, res)
        return res    
    
    def _compute_level_tree_commit(self, cr, uid, ids, child_ids, res, field_names, context=None):
        def recursive_computation(account_id, res, repeated_account_ids=[]):
            currency_obj = self.pool.get('res.currency')
            account = self.browse(cr, uid, account_id)
            for son in account.child_ids:
                if son.id in repeated_account_ids:
                    continue
                res = recursive_computation(son.id, res)
                repeated_account_ids.append(son.id)
                for field in field_names:
                    if account.currency_id.id == son.currency_id.id or field=='quantity_commit':
                        res[account.id][field] += res[son.id][field]
                    else:
                        res[account.id][field] += currency_obj.compute(cr, uid, son.currency_id.id, account.currency_id.id, res[son.id][field], context=context)
            return res
        for account in self.browse(cr, uid, ids, context=context):
            if account.id not in child_ids:
                continue
            res = recursive_computation(account.id, res)
        return res    
    
    def _debit_credit_bal_qtty_plan(self, cr, uid, ids, name, arg, context=None):
        res = {}
        if context is None:
            context = {}
        child_ids = tuple(self.search(cr, uid, [('parent_id', 'child_of', ids)]))
        for i in child_ids:
            res[i] =  {}
            for n in name:
                res[i][n] = 0.0

        if not child_ids:
            return res

        where_date = ''
        where_clause_args = [tuple(child_ids)]
        if context.get('from_date', False):
            where_date += " AND l.date >= %s"
            where_clause_args  += [context['from_date']]
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
                          ) as debit,
                     sum(
                         CASE WHEN l.amount < 0
                         THEN -l.amount
                         ELSE 0.0
                         END
                          ) as credit,
                     COALESCE(SUM(l.amount),0) AS balance,
                     COALESCE(SUM(l.unit_amount),0) AS quantity
              FROM account_analytic_account a
                  LEFT JOIN account_analytic_line_plan l ON (a.id = l.account_id)
              WHERE a.id IN %s
              """ + where_date + """
              GROUP BY a.id""", where_clause_args)
        for ac_id, debit, credit, balance, quantity in cr.fetchall():
            res[ac_id] = {'debit_plan': debit, 'credit_plan': credit, 'balance_plan': balance, 'quantity_plan': quantity}
        return self._compute_level_tree_plan(cr, uid, ids, child_ids, res, ['debit_plan', 'credit_plan', 'balance_plan', 'quantity_plan'], context)

    def _debit_credit_bal_qtty_commit(self, cr, uid, ids, name, arg, context=None):
        res = {}
        if context is None:
            context = {}
        child_ids = tuple(self.search(cr, uid, [('parent_id', 'child_of', ids)]))
        for i in child_ids:
            res[i] =  {}
            for n in name:
                res[i][n] = 0.0

        if not child_ids:
            return res

        where_date = ''
        where_clause_args = [tuple(child_ids)]
        if context.get('from_date', False):
            where_date += " AND l.date >= %s"
            where_clause_args  += [context['from_date']]
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
                          ) as debit,
                     sum(
                         CASE WHEN l.amount < 0
                         THEN -l.amount
                         ELSE 0.0
                         END
                          ) as credit,
                     COALESCE(SUM(l.amount),0) AS balance,
                     COALESCE(SUM(l.unit_amount),0) AS quantity
              FROM account_analytic_account a
                  LEFT JOIN account_analytic_line_commit l ON (a.id = l.account_id)
              WHERE a.id IN %s
              """ + where_date + """
              GROUP BY a.id""", where_clause_args)
        for ac_id, debit, credit, balance, quantity in cr.fetchall():
            res[ac_id] = {'debit_commit': debit, 'credit_commit': credit, 'balance_commit': balance, 'quantity_commit': quantity}
        return self._compute_level_tree_commit(cr, uid, ids, child_ids, res, ['debit_commit', 'credit_commit', 'balance_commit', 'quantity_commit'], context)

    
    _columns = {   
        
        #In case that the parent is deleted, we also delete this entity
        'parent_id': fields.many2one('account.analytic.account', 'Parent Analytic Account', select=2, ondelete='cascade'),
                         
        'balance_plan': fields.function(_debit_credit_bal_qtty_plan, method=True, type='float', string='Planned Balance', multi='debit_credit_bal_qtty_plan', digits_compute=dp.get_precision('Account')),
        'balance_commit': fields.function(_debit_credit_bal_qtty_commit, method=True, type='float', string='Commitment Balance', multi='debit_credit_bal_qtty_commit', digits_compute=dp.get_precision('Account')),
        'debit_plan': fields.function(_debit_credit_bal_qtty_plan, method=True, type='float', string='Planned Debit', multi='debit_credit_bal_qtty_plan', digits_compute=dp.get_precision('Account')),
        'debit_commit': fields.function(_debit_credit_bal_qtty_commit, method=True, type='float', string='Planned Commitments', multi='debit_credit_bal_qtty_commit', digits_compute=dp.get_precision('Account')),
        'credit_plan': fields.function(_debit_credit_bal_qtty_plan, method=True, type='float', string='Planned Credit', multi='debit_credit_bal_qtty_plan', digits_compute=dp.get_precision('Account')),
        'credit_commit': fields.function(_debit_credit_bal_qtty_commit, method=True, type='float', string='Commitments Credit', multi='debit_credit_bal_qtty_commit', digits_compute=dp.get_precision('Account')),
        'state': fields.selection([('draft','Draft'),('ready','Ready'),('open','Open'), ('pending','Pending'),('cancelled', 'Cancelled'),('close','Closed'),('template', 'Template')], 'State', required=True,
                                  help='* When an account is created its in \'Draft\' state.\
                                  \n* When is ready to be used, it can be in \'Ready\' state.\
                                  \n* If any associated partner is there, it can be in \'Open\' state.\
                                  \n* If any pending balance is there it can be in \'Pending\'. \
                                  \n* And finally when all the transactions are over, it can be in \'Close\' state. \
                                  \n* The project can be in either if the states \'Template\' and \'Running\'.\n If it is template then we can make projects based on the template projects. If its in \'Running\' state it is a normal project.\
                                 \n If it is to be reviewed then the state is \'Pending\'.\n When the project is completed the state is set to \'Done\'.'),
        'plan_line_ids': fields.one2many('account.analytic.line.plan', 'account_id', 'Analytic Entries'),
        'commit_line_ids': fields.one2many('account.analytic.line.commit', 'account_id', 'Commitment Analytic Entries'),
                      
     }
    
    _defaults = {
        'state': 'draft',
    }
    
    def set_ready(self, cr, uid, ids, context=None):
        self.write(cr, uid, ids, {'state':'ready'}, context=context)
        return True
    
    def copy(self, cr, uid, id, default=None, context=None):
        if not default:
            default = {}        
        default['plan_line_ids'] = []
        default['commit_line_ids'] = []
        return super(account_analytic_account, self).copy(cr, uid, id, default, context=context)
    
                
account_analytic_account()