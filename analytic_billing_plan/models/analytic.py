# -*- coding: utf-8 -*-
#    Copyright 2015 Matmoz d.o.o. (Matjaž Mozetič)
#    Copyright 2015 Eficent (Jordi Ballester Alomar)
#    Copyright 2017 Luxim d.o.o. (Matjaž Mozetič)
#    License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openerp import fields, models, api


class Analytic(models.Model):
    _inherit = "account.analytic.account"

    deliverable_ids = fields.One2many(
        comodel_name='analytic.billing.plan.line',
        inverse_name='account_id',
        string='Deliverables'
    )

    deliverable_count = fields.Integer(
        compute='_compute_deliverable_count', type='integer'
    )

    @api.depends('deliverable_ids')
    def _compute_deliverable_count(self):
        for record in self:
            record.deliverable_count = len(record.deliverable_ids)
