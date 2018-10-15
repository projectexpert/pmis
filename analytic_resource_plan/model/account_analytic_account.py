# -*- coding: utf-8 -*-
#    Copyright 2017 Matmoz d.o.o. (Matjaž Mozetič)
#    Copyright 2017 Eficent (Jordi Ballester Alomar)
#    Copyright 2017 Luxim d.o.o. (Matjaž Mozetič)
#    License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openerp import fields, models, api


class Analytic(models.Model):
    _inherit = "account.analytic.account"

    resource_ids = fields.One2many(
        comodel_name='analytic.resource.plan.line',
        inverse_name='account_id',
        string='Resources'
    )

    resource_count = fields.Integer(
        compute='_compute_resource_count', type='integer'
    )

    @api.depends('resource_ids')
    def _compute_resource_count(self):
        for record in self:
            record.resource_count = len(record.resource_ids)
