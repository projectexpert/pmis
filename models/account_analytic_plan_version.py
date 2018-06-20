# -*- coding: utf-8 -*-
# Copyright 2015 Eficent Business and IT Consulting Services S.L.
# (Jordi Ballester Alomar)
# Copyright 2016 Matmoz d.o.o.
# (Matjaž Mozetič)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class AccountAnalyticPlanVersion(models.Model):
    _name = 'account.analytic.plan.version'
    _description = 'Analytic Planning Version'

    name = fields.Char(
        'Planning Version Name',
        required=True
    )
    code = fields.Char(
        'Planning Version Code'
    )
    active = fields.Boolean(
        'Active',
        help='''If the active field is set to False, it will allow you to hide
                the analytic planning version without removing it.''',
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

    @api.multi
    @api.constrains('default_committed')
    def _check_default_committed(self):
        for rec in self:
            default_committed = self.search([('default_committed', '=', True)])
            if len(default_committed) > 1:
                raise UserError(
                    _('Only one default commitments version can exist.')
                )
            return

    @api.multi
    @api.constrains('default_plan')
    def _check_default_plan(self):
        for rec in self:
            default_plan = self.search([('default_plan', '=', True)])
            if len(default_plan) > 1:
                raise UserError(
                    _('Only one default plan version can exist.')
                )
            return
