# -*- coding: utf-8 -*-
# © 2014-17 Eficent Business and IT Consulting Services S.L.
# © 2016 Matmoz d.o.o.
# Copyright 2017 Serpent Consulting Services Pvt. Ltd.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class account_analytic_account(models.Model):

    _inherit = "account.analytic.account"

    move_ids = fields.One2many(
        'stock.move',
        'analytic_account_id',
        'Moves for this analytic account',
        readonly=True
    )

    @api.multi
    def copy(self, default=None):
        self.ensure_one()
        default = dict(default or {})
        default['move_ids'] = []
        return super(account_analytic_account, self).copy(default=default)
