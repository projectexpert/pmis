# -*- coding: utf-8 -*-

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
