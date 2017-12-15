# -*- coding: utf-8 -*-
# Copyright (C) 2017 Matmoz d.o.o. (<http://www.matmoz.si>).
# Copyright (C) 2018 Luxim d.o.o. (<https://www.luxim.si>).
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openerp import api, models, fields


class GapAnalysis (models.Model):
    _name = 'change.gap.analysis'
    _description = 'GAP analysis table'

    diagnosis = fields.Char(
        string="Scenario",
        required=False
    )
    deliverable_id = fields.Many2one(
        comodel_name='analytic.billing.plan.line',
        string='Deliverable',
        ondelete='cascade',
        help="Planned deliverable to fill the gap."
    )
    change_id = fields.Many2one(
        comodel_name='change.management.change',
        string='Request',
    )
    project_id = fields.Many2one(
        comodel_name='project.project',
        related='change_id.project_id'
    )
    account_id = fields.Many2one(
        comodel_name='account.analytic.account',
        related='change_id.project_id.analytic_account_id'
    )
