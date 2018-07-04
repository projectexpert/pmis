# -*- coding: utf-8 -*-
# Copyright 2015 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo.addons import decimal_precision as dp
from odoo import api, fields, models


class AccountAnalyticAccount(models.Model):

    _inherit = 'account.analytic.account'

    @api.multi
    def _compute_wip_report(self):
        for account in self:
            all_ids = account.get_child_accounts().keys()
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
            # pylint: disable=sql-injection
            cr.execute(
                """
                SELECT amount, L.id
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
            total_value_line_ids = []
            for (total, line_id) in cr.fetchall():
                account.total_value += total
                total_value_line_ids.append(line_id)
            account.total_value_line_ids = [
                (6, 0, [l for l in total_value_line_ids])]
            # Actual billings to date
            cr.execute(
                """
                SELECT amount, L.id
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
            actual_billings_line_ids = []
            for (total, line_id) in cr.fetchall():
                account.actual_billings += total
                actual_billings_line_ids.append(line_id)

            account.actual_billings_line_ids = [
                (6, 0, [l for l in actual_billings_line_ids])]
            # Actual costs to date
            cr.execute(
                """
                SELECT amount, L.id, AAJ.cost_type
                       FROM account_analytic_line L
                       INNER JOIN account_analytic_journal AAJ
                       ON AAJ.id = L.journal_id
                       INNER JOIN account_account AC
                       ON L.general_account_id = AC.id
                       INNER JOIN account_account_type AT
                       ON AT.id = AC.user_type_id
                       WHERE AT.name in ('Expense', 'Cost of Goods Sold')
                       AND L.account_id IN %s
                """ + where_date + """
                """,
                query_params)
            account.actual_costs = 0
            actual_cost_line_ids = []
            actual_material_line_ids = []
            actual_labor_line_ids = []
            for (total, line_id, cost_type) in cr.fetchall():
                if cost_type in ('material', 'revenue'):
                    account.actual_material_cost -= total
                    actual_material_line_ids.append(line_id)
                elif cost_type == 'labor':
                    account.actual_labor_cost -= total
                    actual_labor_line_ids.append(line_id)
                account.actual_costs -= total
                actual_cost_line_ids.append(line_id)
            account.actual_cost_line_ids = [
                (6, 0, [l for l in actual_cost_line_ids])]
            account.actual_material_line_ids = [
                (6, 0, [l for l in actual_material_line_ids])]
            account.actual_labor_line_ids = [
                (6, 0, [l for l in actual_labor_line_ids])]

            # Total estimated costs
            cr.execute(
                """
                SELECT -amount, L.id
                FROM account_analytic_line_plan AS L
                LEFT JOIN account_analytic_account AS A
                ON L.account_id = A.id
                INNER JOIN account_account AC
                ON L.general_account_id = AC.id
                INNER JOIN account_account_type AT
                ON AT.id = AC.user_type_id
                WHERE AT.name in ('Expense', 'Cost of Goods Sold')
                AND L.account_id IN %s
                AND A.active_analytic_planning_version = L.version_id
                """ + where_date + """
                """,
                query_params
            )
            total_estimated_cost_line_ids = []
            for (total, line_id) in cr.fetchall():
                account.total_estimated_costs += total
                total_estimated_cost_line_ids.append(line_id)
            account.total_estimated_cost_line_ids = [
                (6, 0, [l for l in total_estimated_cost_line_ids])]
            # Estimated costs to complete
            account.estimated_costs_to_complete = (
                account.total_estimated_costs - account.actual_costs)

            # Estimated gross profit
            account.estimated_gross_profit = (
                account.total_value - account.total_estimated_costs)

            # Percent complete
            try:
                account.percent_complete = (
                    (account.actual_costs / account.total_estimated_costs)
                    * 100)
            except ZeroDivisionError:
                account.percent_complete = 0

            # Earned revenue
            account.earned_revenue = (
                account.percent_complete/100 * account.total_value)

            # Over/Under billings
            over_under_billings = (account.actual_billings -
                                   account.earned_revenue)
            account.under_over = over_under_billings

            if over_under_billings > 0:
                account.over_billings = over_under_billings
            else:
                account.under_billings = -1*over_under_billings
            try:
                account.estimated_gross_profit_per = (
                    account.estimated_gross_profit /
                    account.total_value * 100)
            except ZeroDivisionError:
                account.estimated_gross_profit_per = 0
            over_under_billings = (account.under_billings -
                                   account.over_billings)
            account.under_over = over_under_billings
        return True

    total_value = fields.Float(
        compute='_compute_wip_report',
        string='Total Value',
        help="""Total estimated revenue of the contract""",
        digits=dp.get_precision('Account')
    )
    actual_billings = fields.Float(
        compute='_compute_wip_report',
        string='Actual Billings to date',
        help="""Total invoiced amount issued to the customer to date""",
        digits=dp.get_precision('Account')
    )
    actual_costs = fields.Float(
        compute='_compute_wip_report',
        string='Actual Costs to date',
        digits=dp.get_precision('Account')
    )
    actual_material_cost = fields.Float(
        compute='_compute_wip_report',
        string='Material Costs to date',
        digits=dp.get_precision('Account')
    )
    actual_labor_cost = fields.Float(
        compute='_compute_wip_report',
        string='Labor Costs to date',
        digits=dp.get_precision('Account')
    )
    total_estimated_costs = fields.Float(
        compute='_compute_wip_report',
        string='Total Estimated Costs',
        digits=dp.get_precision('Account')
    )
    estimated_costs_to_complete = fields.Float(
        compute='_compute_wip_report',
        string='Estimated Costs to Complete',
        help="""Total Estimated Costs – Actual Costs to Date""",
        digits=dp.get_precision('Account')
    )
    estimated_gross_profit = fields.Float(
        compute='_compute_wip_report',
        string='Estimated Gross Profit',
        help="""Total Value – Total Estimated Costs""",
        digits=dp.get_precision('Account')
    )
    estimated_gross_profit_per = fields.Float(
        compute='_compute_wip_report',
        string='Estimated Gross Profit',
        help="""Total Value – Total Estimated Costs""",
        digits=dp.get_precision('Account')
    )
    percent_complete = fields.Float(
        compute='_compute_wip_report',
        string='Percent Complete',
        help="Actual Costs to Date / Total Estimated Costs",
        digits=dp.get_precision('Account')
    )
    earned_revenue = fields.Float(
        compute='_compute_wip_report',
        string='Earned Revenue to date',
        help="Percent Complete * Total Estimated Revenue",
        digits=dp.get_precision('Account')
    )
    over_billings = fields.Float(
        compute='_compute_wip_report',
        string='Over billings',
        help="""Total Billings on Contract – Earned Revenue to Date
                (when > 0 )""",
        digits=dp.get_precision('Account')
    )
    under_billings = fields.Float(
        compute='_compute_wip_report',
        string='Under billings',
        help="""Total Billings on Contract – Earned Revenue to Date
                (when < 0 )""",
        digits=dp.get_precision('Account')
    )
    under_over = fields.Float(
        compute='_compute_wip_report',
        string='Under over',
        help="""Billings in excess of costs""",
        digits=dp.get_precision('Account')
    )
    actual_billings_line_ids = fields.Many2many(
        comodel_name="account.analytic.line",
        compute='_compute_wip_report',
        string='Detail',
    )
    actual_cost_line_ids = fields.Many2many(
        comodel_name="account.analytic.line",
        compute='_compute_wip_report',
        string='Detail',
    )
    actual_material_line_ids = fields.Many2many(
        comodel_name="account.analytic.line",
        compute='_compute_wip_report',
        string='Detail',
    )
    actual_labor_line_ids = fields.Many2many(
        comodel_name="account.analytic.line",
        compute='_compute_wip_report',
        string='Detail',
    )
    total_estimated_cost_line_ids = fields.Many2many(
        comodel_name="account.analytic.line.plan",
        compute='_compute_wip_report',
        string='Detail',
    )
    total_value_line_ids = fields.Many2many(
        comodel_name="account.analytic.line.plan",
        compute='_compute_wip_report',
        string='Detail',
    )

    @api.multi
    def action_open_analytic_lines(self):
        line = self
        bill_lines = [x.id for x in line.actual_billings_line_ids]
        res = self.env['ir.actions.act_window'].for_xml_id(
            'analytic', 'account_analytic_line_action_entries')
        res['domain'] = "[('id', 'in', ["+','.join(
            map(str, bill_lines))+"])]"
        return res

    @api.multi
    def action_open_cost_lines(self):
        line = self
        bill_lines = [x.id for x in line.actual_cost_line_ids]
        res = self.env['ir.actions.act_window'].for_xml_id(
            'analytic', 'account_analytic_line_action_entries')
        res['domain'] = "[('id', 'in', ["+','.join(
            map(str, bill_lines))+"])]"
        return res

    @api.multi
    def action_open_material_lines(self):
        line = self
        bill_lines = [x.id for x in line.actual_material_line_ids]
        res = self.env['ir.actions.act_window'].for_xml_id(
            'analytic', 'account_analytic_line_action_entries')
        res['domain'] = "[('id', 'in', ["+','.join(
            map(str, bill_lines))+"])]"
        return res

    @api.multi
    def action_open_labor_lines(self):
        """
        :return dict: dictionary value for created view
        """
        line = self
        bill_lines = [x.id for x in line.actual_labor_line_ids]
        res = self.env['ir.actions.act_window'].for_xml_id(
            'analytic', 'account_analytic_line_action_entries')
        res['domain'] = "[('id', 'in', ["+','.join(
            map(str, bill_lines))+"])]"
        return res

    @api.multi
    def action_open_total_estimated_cost_lines(self):
        line = self
        bill_lines = [x.id for x in line.total_estimated_cost_line_ids]
        res = self.env['ir.actions.act_window'].for_xml_id(
            'analytic_plan', 'action_account_analytic_line_plan_form')
        res['domain'] = "[('id', 'in', ["+','.join(
            map(str, bill_lines))+"])]"
        return res

    @api.multi
    def action_open_totalvalue_lines(self):
        line = self
        bill_lines = [x.id for x in line.total_value_line_ids]
        res = self.env['ir.actions.act_window'].for_xml_id(
            'analytic_plan', 'action_account_analytic_line_plan_form')
        res['domain'] = "[('id', 'in', ["+','.join(
            map(str, bill_lines))+"])]"
        return res
