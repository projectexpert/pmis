# -*- coding: utf-8 -*-
# © 2017 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from openerp import api, fields, models


class StockChangeProductQty(models.TransientModel):
    _inherit = "stock.change.product.qty"

    @api.multi
    @api.depends('location_id')
    def _compute_analytic_account_id(self):
        for wiz in self:
            if wiz.location_id.analytic_account_id:
                wiz.analytic_account_id = wiz.location_id.analytic_account_id.id,
        return True

    analytic_account_id = fields.Many2one(
        comodel_name="account.analytic.account",
        compute=_compute_analytic_account_id,
        string="Analytic Account")
