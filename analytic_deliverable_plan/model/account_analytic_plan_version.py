# -*- coding: utf-8 -*-
#    Copyright 2016 MATMOZ, Slovenia (Matjaž Mozetič)
#    Copyright 2018 EFICENT (Jordi Ballester Alomar)
#    Copyright 2018 LUXIM, Slovenia (Matjaž Mozetič)
#    Together as the Project Expert Team
#    License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo.tools.translate import _
from odoo import api, fields, models
from odoo.exceptions import ValidationError


class AccountAnalyticPlanVersion(models.Model):
    _inherit = 'account.analytic.plan.version'

    default_deliverable_plan = fields.Boolean(
        'Default for deliverable plan',
        default=False
    )

    @api.multi
    @api.constrains('default_deliverable_plan')
    def _check_default_deliverable(self):
        for rec in self:
            default_res_plan = self.search(
                [('default_deliverable_plan', '=', True)])
            if len(default_res_plan) > 1:
                raise ValidationError(
                    _('Only one default for deliverable plan version can'
                      ' exist.'))
