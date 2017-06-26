# -*- coding: utf-8 -*-
# © 2017 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from openerp import api, fields, models, _
from openerp.tools import float_compare, float_round, DEFAULT_SERVER_DATETIME_FORMAT
from openerp.exceptions import ValidationError


class StockQuant(models.Model):
    _inherit = "stock.quant"

    @api.multi
    @api.constrains('analytic_account_id', 'location_id')
    def _check_analytic_account(self):
        for quant in self:
            if quant.analytic_account_id:
                analytic = quant.analytic_account_id
                location = quant.location_id
                parent = location.location_id
                if parent.usage != 'view' \
                        and parent.analytic_account_id != analytic:
                    raise ValidationError(_("Wrong analytic account in the "
                                            "quant"))
        return True
