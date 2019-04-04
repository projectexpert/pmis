#    Copyright 2016 MATMOZ, Slovenia (Matjaž Mozetič)
#    Copyright 2018 EFICENT (Jordi Ballester Alomar)
#    Copyright 2018 LUXIM, Slovenia (Matjaž Mozetič)
#    Together as the Project Expert Team
#    License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    revenue_analytic_plan_journal_id = fields.Many2one(
        comodel_name='account.analytic.plan.journal',
        string='Revenue Plan Journal',
        ondelete='restrict'
    )

    expense_analytic_plan_journal_id = fields.Many2one(
        'account.analytic.plan.journal',
        'Expense Plan Journal',
        ondelete='restrict'
    )
