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
import decimal_precision as dp
from osv import fields, osv

class account_analytic_account(osv.osv):
    
    _inherit = 'account.analytic.account'
    
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
                  LEFT JOIN account_analytic_plan_version v ON (l.version_id = v.id)
              WHERE a.id IN %s
              AND v.default_plan = True
              """ + where_date + """             
              GROUP BY a.id""", where_clause_args)
        
        for row in cr.dictfetchall():
            res[row['id']] = {}
            for field in fields:
                res[row['id']][field] = row[field]
        return self._compute_level_tree_plan(cr, uid, ids, child_ids, res, fields, context)

    _columns = {   
        
        #In case that the parent is deleted, we also delete this entity
        'parent_id': fields.many2one('account.analytic.account',
                                     'Parent Analytic Account',
                                     select=2, ondelete='cascade'),
                         
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
        'state': fields.selection([('draft', 'Draft'),
                                   ('ready', 'Ready'),
                                   ('open', 'Open'),
                                   ('pending', 'Pending'),
                                   ('cancelled', 'Cancelled'),
                                   ('close', 'Closed'),
                                   ('template', 'Template')],
                                  'State', required=True,
                                  help='* When an account is created its in \'Draft\' state.\
                                  \n* When is ready to be used, it can be in \'Ready\' state.\
                                  \n* If any associated partner is there, it can be in \'Open\' state.\
                                  \n* If any pending balance is there it can be in \'Pending\'. \
                                  \n* And finally when all the transactions are over, it can be in \'Close\' state. \
                                  \n* The project can be in either if the states \'Template\' and \'Running\'.'
                                       '\n If it is template then we can make projects based on the template projects. '
                                       'If its in \'Running\' state it is a normal project.\
                                  \n If it is to be reviewed then the state is \'Pending\'.'
                                       '\n When the project is completed the state is set to \'Done\'.'),
        'plan_line_ids': fields.one2many('account.analytic.line.plan',
                                         'account_id',
                                         'Analytic Entries'),
     }
    
    _defaults = {
        'state': 'draft',
    }
    
    def set_ready(self, cr, uid, ids, context=None):
        self.write(cr, uid, ids, {'state': 'ready'}, context=context)
        return True
    
    def copy(self, cr, uid, id, default=None, context=None):
        if default is None:
            default = {}        
        default['plan_line_ids'] = []        
        return super(account_analytic_account, self).copy(cr, uid, id, default, context=context)
    
                
account_analytic_account()