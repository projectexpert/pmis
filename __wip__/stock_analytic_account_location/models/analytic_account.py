# -*- coding: utf-8 -*-
# © 2017 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from openerp import api, fields, models
from openerp.exceptions import ValidationError

class AccountAnalyticAccount(models.Model):
    _inherit = 'account.analytic.account'

    @api.multi
    @api.constrains('location_id')
    def _check_location(self):
        for analytic in self:
            if analytic.location_id:
                if analytic.location_id.analytic_account_id != analytic:
                    return ValidationError("The location does not belong to "
                                           "this project")
        return True
