# -*- coding: utf-8 -*-
#    Copyright 2017 Matmoz d.o.o. (Matjaž Mozetič)
#    Copyright 2017 Eficent (Jordi Ballester Alomar)
#    Copyright 2017 Luxim d.o.o. (Matjaž Mozetič)
#    License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openerp import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    expense_analytic_plan_journal_id = fields.Many2one(
        'account.analytic.plan.journal',
        'Expense Plan Journal',
        ondelete='restrict'
    )
