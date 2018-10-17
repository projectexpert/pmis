# -*- coding: utf-8 -*-
#    Copyright 2015 MATMOZ, Slovenia (Matjaž Mozetič)
#    Copyright 2015 EFICENT (Jordi Ballester Alomar)
#    Copyright 2018 LUXIM, Slovenia (Matjaž Mozetič)
#    Together as the Project Expert Team
#    License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class AccountAnalyticLinePlan(models.Model):
    _inherit = 'account.analytic.line.plan'

    deliverable_plan_id = fields.Many2one(
        comodel_name='analytic.deliverable.plan.line',
        string='Deliverable Plan Line',
        copy=False,
        ondelete='cascade'
    )
