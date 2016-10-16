# -*- coding: utf-8 -*-
# © 2015 Eficent Business and IT Consulting Services S.L.
# (Jordi Ballester Alomar)
#
# © 2016 Matmoz d.o.o.
# (Matjaž Mozetič)
#
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openerp import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    revenue_analytic_plan_journal_id = fields.Many2one(
        comodel_name='account.analytic.plan.journal',
        string='Revenue Plan Journal',
        ondelete='restrict'
    )
