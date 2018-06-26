# -*- coding: utf-8 -*-
# Copyright 2017 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, models, _
from odoo.exceptions import ValidationError


class StockQuant(models.Model):
    _inherit = "stock.quant"

    @api.multi
    @api.constrains('analytic_account_id', 'location_id')
    def _check_analytic_account(self):
        for quant in self:
            if quant.analytic_account_id:
                analytic = quant.analytic_account_id
                location = quant.location_id
                if location.analytic_account_id != analytic:
                    raise ValidationError(
                        _('Wrong analytic account in the quant'))
        return True
