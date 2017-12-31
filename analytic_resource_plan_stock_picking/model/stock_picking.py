# -*- coding: utf-8 -*-
# © 2017 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openerp import fields, models


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    analytic_resource_plan_line_id = fields.Many2one(
            'analytic.resource.plan.line', "Resource Plan Line", readonly=True)
