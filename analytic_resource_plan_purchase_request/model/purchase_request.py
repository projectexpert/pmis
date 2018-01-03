# -*- coding: utf-8 -*-
#    Copyright 2017 Matmoz d.o.o. (Matjaž Mozetič)
#    Copyright 2017 Eficent (Jordi Ballester Alomar)
#    Copyright 2017 Luxim d.o.o. (Matjaž Mozetič)
#    License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openerp import fields, models


class PurchaseRequestLine(models.Model):

    _inherit = 'purchase.request.line'

    analytic_resource_plan_lines = fields.Many2many(
        comodel_name='analytic.resource.plan.line',
        string='Analytic Planning Lines'
    )
