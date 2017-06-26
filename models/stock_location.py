# -*- coding: utf-8 -*-
# © 2017 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from openerp import api, fields, models, _
from openerp.tools import float_compare, float_round, DEFAULT_SERVER_DATETIME_FORMAT
from openerp.exceptions import ValidationError


class StockLocation(models.Model):
    _inherit = "stock.location"

    analytic_account_id = fields.Many2one('account.analytic.account',
                                          'Analytic Account',
                                          copy=False)

    @api.multi
    @api.constrains('analytic_account_id')
    def _check_analytic_account(self):
        for loc in self:
            if loc.analytic_account_id:
                analytic = loc.analytic_account_id
                if loc.location_id:
                    parent = loc.location_id
                    if parent.usage != 'view' \
                            and parent.analytic_account_id != analytic:
                        raise ValidationError(_("Sublocations can only be "
                                                "related to the same project"))
        return True
