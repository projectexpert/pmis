# -*- coding: utf-8 -*-
# Copyright 2017 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    expense_analytic_plan_journal_id = fields.Many2one(
        'account.analytic.plan.journal',
        'Expense Plan Journal',
        ondelete='restrict'
    )
    revenue_analytic_plan_journal_id = fields.Many2one(
        comodel_name='account.analytic.plan.journal',
        string='Revenue Plan Journal',
        ondelete='restrict'
    )
