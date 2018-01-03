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

    def _wip_report(self, cr, uid, ids, fields, arg, context=None):
        res = {}
        if context is None:
            context = {}

        for account in self.browse(cr, uid, ids, context=context):
            all_ids = self.get_child_accounts(
                cr, uid, [account.id], context=context).keys()

            res[account.id] = {'total_value': 0,
                               'actual_billings': 0,
                               'actual_costs': 0,
                               'total_estimated_costs': 0,
                               'estimated_costs_to_complete': 0,
                               'estimated_gross_profit': 0,
                               'percent_complete': 0,
                               'earned_revenue': 0,
                               'over_billings': 0,
                               'under_billings': 0,
                               }

            # Total Value
            query_params = [tuple(all_ids)]
            where_date = ''
            if context.get('from_date', False):
                where_date += " AND l.date >= %s"
                query_params += [context['from_date']]
            if context.get('to_date', False):
                where_date += " AND l.date <= %s"
                query_params += [context['to_date']]
            cr.execute(
                """
                SELECT COALESCE(sum(amount),0.0) AS total_value
                FROM account_analytic_line_plan AS L
                LEFT JOIN account_analytic_account AS A
                ON L.account_id = A.id
                INNER JOIN account_account AC
                ON L.general_account_id = AC.id
                INNER JOIN account_account_type AT
                ON AT.id = AC.user_type
                WHERE AT.report_type = 'income'
                AND l.account_id IN %s
                AND a.active_analytic_planning_version = l.version_id
                """ + where_date + """
                """,
                query_params
            )
            val = cr.fetchone()[0] or 0
            res[account.id]['total_value'] = val

            # Actual billings to date
            cr.execute(
                """
                SELECT COALESCE(sum(amount),0.0)
                FROM account_analytic_line L
                INNER JOIN account_account AC
                ON L.general_account_id = AC.id
                INNER JOIN account_account_type AT
                ON AT.id = AC.user_type
                WHERE AT.report_type = 'income'
                AND L.account_id IN %s
                """ + where_date + """
                """, query_params
            )
            val = cr.fetchone()[0] or 0
            res[account.id]['actual_billings'] = val

            # Actual costs to date
            cr.execute(
                """
                SELECT COALESCE(-1*sum(amount),0.0)
                FROM account_analytic_line L
                INNER JOIN account_account AC
                ON L.general_account_id = AC.id
                INNER JOIN account_account_type AT
                ON AT.id = AC.user_type
                WHERE AT.report_type = 'expense'
                AND L.account_id IN %s
                """ + where_date + """
                """, query_params
            )
            val = cr.fetchone()[0] or 0
            res[account.id]['actual_costs'] = val

            # Total estimated costs
            cr.execute(
                """
                SELECT COALESCE(-1*sum(amount),0.0) AS total_value
                FROM account_analytic_line_plan AS L
                LEFT JOIN account_analytic_account AS A
                ON L.account_id = A.id
                INNER JOIN account_account AC
                ON L.general_account_id = AC.id
                INNER JOIN account_account_type AT
                ON AT.id = AC.user_type
                WHERE AT.report_type = 'expense'
                AND L.account_id IN %s
                AND A.active_analytic_planning_version = L.version_id
                """ + where_date + """
                """,
                query_params
            )
            val = cr.fetchone()[0] or 0
            res[account.id]['total_estimated_costs'] = val

            # Estimated costs to complete
            res[account.id]['estimated_costs_to_complete'] = (
                res[account.id]['total_estimated_costs'] - res[
                    account.id]['actual_costs']
            )

            # Estimated gross profit
            res[account.id]['estimated_gross_profit'] = (
                res[account.id]['total_value'] - res[account.id][
                    'total_estimated_costs']
            )

            # Percent complete
            try:
                res[account.id]['percent_complete'] = (
                    (res[account.id]['actual_costs'] / res[account.id][
                        'total_estimated_costs']) * 100
                )
            except ZeroDivisionError:
                res[account.id]['percent_complete'] = 0

            # Earned revenue
            res[account.id]['earned_revenue'] = (
                res[account.id]['percent_complete']/100 * res[account.id][
                    'total_value']
            )

            # Over/Under billings
            over_under_billings = res[account.id]['actual_billings'] - res[
                account.id]['earned_revenue']
            if over_under_billings > 0:
                res[account.id]['over_billings'] = over_under_billings
            else:
                res[account.id]['under_billings'] = -1*over_under_billings

        return res

    _columns = {

        'total_value': fields.function(
                _wip_report, method=True, type='float', string='Total Value',
                multi='wip_report',
                help="Total estimated revenue of the contract",
                digits_compute=dp.get_precision('Account')),

        'actual_billings': fields.function(
                _wip_report, method=True, type='float',
                string='Actual Billings to date', multi='wip_report',
                help="Total invoiced amount issued to the customer to date",
                digits_compute=dp.get_precision('Account')),

        'actual_costs': fields.function(
                _wip_report, method=True, type='float',
                string='Actual Costs to date', multi='wip_report',
                digits_compute=dp.get_precision('Account')),

        'total_estimated_costs': fields.function(
                _wip_report, method=True, type='float',
                string='Total Estimated Costs', multi='wip_report',
                digits_compute=dp.get_precision('Account')),

        'estimated_costs_to_complete': fields.function(
                _wip_report, method=True, type='float',
                string='Estimated Costs to Complete',
                help="Total Estimated Costs – Actual Costs to Date",
                multi='wip_report', digits_compute=dp.get_precision(
                        'Account')),

        'estimated_gross_profit': fields.function(
                _wip_report, method=True, type='float',
                string='Estimated Gross Profit',
                help="Total Value – Total Estimated Costs",
                multi='wip_report', digits_compute=dp.get_precision(
                        'Account')),

        'percent_complete': fields.function(
                _wip_report, method=True, type='float',
                string='Percent Complete',
                help="Actual Costs to Date / Total Estimated Costs",
                multi='wip_report', digits_compute=dp.get_precision(
                        'Account')),

        'earned_revenue': fields.function(
                _wip_report, method=True, type='float',
                string='Earned Revenue to date',
                help="Percent Complete * Total Estimated Revenue",
                multi='wip_report', digits_compute=dp.get_precision(
                        'Account')),

        'over_billings': fields.function(
                _wip_report, method=True, type='float', string='Over billings',
                help="Total Billings on Contract – Earned Revenue to Date "
                     "(when > 0 )", multi='wip_report',
                digits_compute=dp.get_precision('Account')),

        'under_billings': fields.function(
                _wip_report, method=True, type='float',
                string='Under billings',
                help="Total Billings on Contract – Earned Revenue to Date "
                     "(when < 0 )", multi='wip_report',
                digits_compute=dp.get_precision('Account')),
        }
