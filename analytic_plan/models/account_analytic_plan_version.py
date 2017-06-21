# -*- coding: utf-8 -*-
# © 2015 Eficent Business and IT Consulting Services S.L.
# (Jordi Ballester Alomar)
#
# © 2016 Matmoz d.o.o.
# (Matjaž Mozetič)
#
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openerp.tools.translate import _
from openerp import api, fields, models
from openerp.exceptions import Warning as UserError


class AccountAnalyticPlanVersion(models.Model):
    _name = 'account.analytic.plan.version'
    _description = 'Analytic Planning Version'

    name = fields.Char(
        'Planning Version Name', required=True
    )
    code = fields.Char(
        'Planning Version Code'
    )
    active = fields.Boolean(
        'Active',
        help='If the active '
             'field is set to False, '
             'it will allow you to hide '
             'the analytic planning version '
             'without removing it.',
        default=True
    )
    notes = fields.Text(
        'Notes'
    )
    company_id = fields.Many2one(
        'res.company',
        'Company',
        required=True,
        default=lambda self:
            self.env['res.users'].browse(self._uid).company_id.id
    )
    default_committed = fields.Boolean(
        'Default version for committed costs',
        default=False
    )
    default_plan = fields.Boolean(
        'Default planning version',
        default=False
    )

    @api.model
    def _check_default_committed(self, vals):
        if 'default_committed' in vals:
            if vals['default_committed'] is True:
                other_default_committed = self.search(
                    [('default_committed', '=', True)]
                )
                if other_default_committed:
                    raise UserError(
                        _(
                            'Only one default commitments '
                            'version can exist.'
                        )
                    )

    @api.model
    def _check_default_plan(self, vals):
        if 'default_plan' in vals:
            if vals['default_plan'] is True:
                other_default_plan = self.search(
                    [('default_plan', '=', True)]
                )
                if other_default_plan:
                    raise UserError(
                        _(
                            'Only one default plan version '
                            'can exist.'
                        )
                    )

    @api.model
    def create(self, vals):
        self._check_default_committed(vals)
        self._check_default_plan(vals)
        res = super(AccountAnalyticPlanVersion, self).create(vals)
        return res

    @api.multi
    def write(self, vals):
        self._check_default_committed(vals)
        self._check_default_plan(vals)
        return super(AccountAnalyticPlanVersion, self).write(vals)
