# -*- coding: utf-8 -*-
# © 2015 Eficent Business and IT Consulting Services S.L.
# (Jordi Ballester Alomar)
#
# © 2015 Serpent Consulting Services Pvt. Ltd.
# (Sudhir Arya)
#
# © 2016 Matmoz d.o.o.
# (Matjaž Mozetič)
#
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openerp.tools.translate import _
from openerp import api, fields, models
from openerp.exceptions import Warning as UserError


class AccountAnalyticPlanVersion(models.Model):
    _inherit = 'account.analytic.plan.version'

    default_resource_plan = fields.Boolean(
        'Default for resource plan',
        default=False
    )

    # TODO Solve TypeError: can only concatenate list (not "NoneType") to list
    @api.model
    def _check_default_resource(self, vals):
        if 'default_resource_plan' in vals:
            if vals['default_resource_plan'] is True:
                other_default_resource = self.search(
                    [('default_resource_plan', '=', True)]
                )
                if other_default_resource:
                    raise UserError(
                        _(
                            'Only one default for resource '
                            'plan version can exist.'
                        )
                    )

    @api.model
    def create(self, vals):
        self._check_default_resource(vals)
        res = super(AccountAnalyticPlanVersion, self).create(vals)
        return res

    @api.multi
    def write(self, vals):
        self._check_default_resource(vals)
        return super(AccountAnalyticPlanVersion, self).write(vals)
