# -*- coding: utf-8 -*-

from openerp import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    revenue_analytic_plan_journal_id = fields.Many2one(
        comodel_name='account.analytic.plan.journal',
        string='Revenue Plan Journal',
        ondelete='restrict'
    )
