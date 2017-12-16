# -*- coding: utf-8 -*-

from openerp import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    expense_analytic_plan_journal_id = fields.Many2one(
        'account.analytic.plan.journal',
        'Expense Plan Journal',
        ondelete='restrict'
    )
