# -*- coding: utf-8 -*-
# Copyright 2014-17 Eficent Business and IT Consulting Services S.L.
# Copyright 2016 Matmoz d.o.o.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class AccountAnalyticAccount(models.Model):
    _inherit = 'account.analytic.account'

    @api.model
    def _default_dest_address(self):
        partner_id = self.env.context.get('partner_id', False)
        if partner_id:
            return self.env['res.partner'].address_get(
                [partner_id], ['delivery']
            )['delivery'],
        else:
            return False

    location_id = fields.Many2one(
        'stock.location',
        'Default Stock Location',
        domain=[('usage', '<>', 'view')]
    )
    dest_address_id = fields.Many2one(
        'res.partner',
        'Delivery Address',
        default=_default_dest_address,
        help="""Delivery address for the current contract project."""
    )
