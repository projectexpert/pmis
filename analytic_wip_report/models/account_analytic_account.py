# -*- coding: utf-8 -*-
# Copyright 2015 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo.addons import decimal_precision as dp
from odoo import api, fields, models


class AccountAnalyticAccount(models.Model):

    _inherit = 'account.analytic.account'

    @api.multi
    def _wip_report(self):
        res = {}
        for account in self:
            all_ids = self.get_child_accounts().keys()
            res[account.id] = {
                'total_value': 0,
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
            context = self._context
            cr = self._cr
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
                ON AT.id = AC.user_type_id
                WHERE AT.name in ('Income', 'Other Income')
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
                ON AT.id = AC.user_type_id
                WHERE AT.name in ('Income', 'Other Income')
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
                ON AT.id = AC.user_type_id
                WHERE AT.name in ('Expenses', 'Depreciation',
                'Cost of Revenue')
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
                ON AT.id = AC.user_type_id
                WHERE AT.name in ('Expenses', 'Depreciation',
                'Cost of Revenue')
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

    total_value = fields.Float(
        compute='_wip_report',
        string='Total Value',
        help="""Total estimated revenue of the contract""",
        digits=dp.get_precision('Account')
    )
    actual_billings = fields.Float(
        compute='_wip_report',
        string='Actual Billings to date',
        help="""Total invoiced amount issued to the customer to date""",
        digits=dp.get_precision('Account')
    )
    actual_costs = fields.Float(
        compute='_wip_report',
        string='Actual Costs to date',
        digits=dp.get_precision('Account')
    )
    total_estimated_costs = fields.Float(
        compute='_wip_report',
        string='Total Estimated Costs',
        digits=dp.get_precision('Account')
    )
    estimated_costs_to_complete = fields.Float(
        compute='_wip_report',
        string='Estimated Costs to Complete',
        help="""Total Estimated Costs – Actual Costs to Date""",
        digits=dp.get_precision('Account')
    )
    estimated_gross_profit = fields.Float(
        compute='_wip_report',
        string='Estimated Gross Profit',
        help="""Total Value – Total Estimated Costs""",
        digits=dp.get_precision('Account')
    )
    percent_complete = fields.Float(
        compute='_wip_report',
        string='Percent Complete',
        help="Actual Costs to Date / Total Estimated Costs",
        digits=dp.get_precision('Account')
    )
    earned_revenue = fields.Float(
        compute='_wip_report',
        string='Earned Revenue to date',
        help="Percent Complete * Total Estimated Revenue",
        digits=dp.get_precision('Account')
    )
    over_billings = fields.Float(
        compute='_wip_report',
        string='Over billings',
        help="""Total Billings on Contract – Earned Revenue to Date
                (when > 0 )""",
        digits=dp.get_precision('Account')
    )
    under_billings = fields.Float(
        compute='_wip_report',
        string='Under billings',
        help="""Total Billings on Contract – Earned Revenue to Date
                (when < 0 )""",
        digits=dp.get_precision('Account')
    )
