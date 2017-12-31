# -*- coding: utf-8 -*-
# Copyright 2017 Eficent Business and IT Consulting Services S.L.
# Copyright 2017 Matmoz d.o.o.
# Copyright 2017 Luxim d.o.o.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openerp import fields, models


class StockPicking(models.Model):

    _inherit = "stock.picking"

    analytic_account_ids = fields.Many2one(
        'account.analytic.account',
        related='move_lines.analytic_account_id',
        string='Analytic Account',
        readonly=True
    )
    analytic_account_user_ids = fields.Many2one(
        'res.users',
        related='move_lines.analytic_account_user_id',
        string='Project Manager',
        readonly=True
    )
