# -*- coding: utf-8 -*-
# Copyright 2014-17 Eficent Business and IT Consulting Services S.L.
# Copyright 2016 Matmoz d.o.o.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class StockQuant(models.Model):

    _inherit = "stock.quant"

    analytic_account_id = fields.Many2one(
        'account.analytic.account',
        'Analytic Account'
    )

    @api.model
    def _quant_create_from_move(self, qty, move, lot_id=False, owner_id=False,
                                src_package_id=False, dest_package_id=False,
                                force_location_from=False,
                                force_location_to=False):
        quant = super(StockQuant, self).\
            _quant_create_from_move(qty, move, lot_id=lot_id,
                                    owner_id=owner_id,
                                    src_package_id=src_package_id,
                                    dest_package_id=dest_package_id,
                                    force_location_from=force_location_from,
                                    force_location_to=force_location_to)
        if move.analytic_account_id:
            quant.write({'analytic_account_id': move.analytic_account_id.id})
        return quant

    def _quants_get_reservation_domain(self, move, pack_operation_id=False,
                                       lot_id=False, company_id=False,
                                       initial_domain=None):
        domain = super(StockQuant, self)._quants_get_reservation_domain(
            move, pack_operation_id=pack_operation_id, lot_id=lot_id,
            company_id=company_id, initial_domain=initial_domain)
        if move.analytic_account_id:
            domain += [
                ('analytic_account_id', '=', move.analytic_account_id.id)]
        return domain
