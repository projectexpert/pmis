# -*- coding: utf-8 -*-
#    Copyright 2016 MATMOZ, Slovenia (Matjaž Mozetič)
#    Copyright 2018 EFICENT (Jordi Ballester Alomar)
#    Copyright 2018 LUXIM, Slovenia (Matjaž Mozetič)
#    Together as the Project Expert Team
#    License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models, api
from odoo.addons import decimal_precision as dp


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

    resource_total_cost = fields.Float(
        string='Total Cost',
        digit=dp.get_precision('Account'),
        compute='_compute_resource_total_cost'
    )

    @api.depends('resource_ids')
    def _compute_resource_count(self):
        for record in self:
            record.resource_count = len(record.resource_ids)

    @api.multi
    def _compute_resource_total_cost(self):
        for record in self:
            record.resource_total_cost = sum(
                resource.price_total for resource in
                record.resource_ids
            )
