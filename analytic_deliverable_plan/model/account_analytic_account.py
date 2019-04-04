#    Copyright 2016 MATMOZ, Slovenia (Matjaž Mozetič)
#    Copyright 2018 EFICENT (Jordi Ballester Alomar)
#    Copyright 2018 LUXIM, Slovenia (Matjaž Mozetič)
#    Together as the Project Expert Team
#    License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models, api
from odoo.addons import decimal_precision as dp


class Analytic(models.Model):
    _inherit = "account.analytic.account"

    deliverable_ids = fields.One2many(
        comodel_name='analytic.deliverable.plan.line',
        inverse_name='account_id',
        string='Deliverables'
    )

    deliverable_count = fields.Integer(
        compute='_compute_deliverable_count', type='integer'
    )

    deliverable_total_revenue = fields.Float(
        string='Total Revenue',
        digit=dp.get_precision('Account'),
        compute='_compute_total_revenue'
    )

    @api.depends('deliverable_ids')
    def _compute_deliverable_count(self):
        for record in self:
            record.deliverable_count = len(record.deliverable_ids)

    @api.multi
    def _compute_total_revenue(self):
        for record in self:
            record.deliverable_total_revenue = sum(
                deliverable.price_total for deliverable in
                record.deliverable_ids
            )
