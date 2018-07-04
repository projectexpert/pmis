# -*- coding: utf-8 -*-
# Copyright 2014-17 Eficent Business and IT Consulting Services S.L.
# Copyright 2016 Matmoz d.o.o.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models


class Product(models.Model):

    _inherit = "product.product"

    def _get_domain_locations(self):
        if self._context.get('analytic_account_id'):
            locations = self.env['stock.location'].search(
                [('analytic_account_id', '=', self._context.get(
                    'analytic_account_id'))]).ids
            dom_loc_out = dom_quant = [('location_id', 'in', locations)]
            dom_loc_in = [('location_dest_id', 'in', locations)]
            return (dom_quant, dom_loc_in, dom_loc_out)
        elif self._context.get('analytic_account_id_out'):
            locations = self.env['stock.location'].search(
                [('analytic_account_id', '=', self._context.get(
                    'analytic_account_id_out'))]).ids
            customer_locations = self.env['stock.location'].search(
                [('usage', '=', 'customer')]).ids
            dom_loc_out = [('location_dest_id', 'in', locations),
                           ('location_id', 'in', customer_locations), ]
            dom_loc_in = [('location_dest_id', 'in', customer_locations),
                          ('location_id', 'in', locations), ]
            dom_quant = [
                ('location_id', 'in', customer_locations),
                ('analytic_account_id', '=',
                 self._context.get('analytic_account_id_out'))
            ]
            return (dom_quant, dom_loc_in, dom_loc_out)
        else:
            return super(Product, self)._get_domain_locations()
