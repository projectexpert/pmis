# -*- coding: utf-8 -*-
# © 2014-17 Eficent Business and IT Consulting Services S.L.
# © 2016 Matmoz d.o.o.
# Copyright 2017 Serpent Consulting Services Pvt. Ltd.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class StockMove(models.Model):

    _inherit = "stock.move"

    analytic_account_user_id = fields.Many2one(
        'res.users',
        related='analytic_account_id.partner_id.user_id',
        store=True,
        readonly=True
    )


class StockScrap(models.Model):

    _inherit = 'stock.scrap'

    def _prepare_move_values(self):
        values = super(StockScrap, self)._prepare_move_values()
        values.update({
            'analytic_account_id': self.move_id.analytic_account_id.id
        })
        return values
