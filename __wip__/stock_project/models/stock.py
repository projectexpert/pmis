# -*- coding: utf-8 -*-
# © 2015 Eficent Business and IT Consulting Services S.L.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from openerp import fields, models, api


class StockMove(models.Model):
    _inherit = "stock.move"

    project_id = fields.Many2one(
        string='Project',
        comodel_name='project.project',
    )


class StockQuant(models.Model):

    _inherit = "stock.quant"

    @api.model
    def _prepare_account_move_line(self, move, qty, cost,
                                   credit_account_id, debit_account_id,
                                   context=None):
        res = super(StockQuant,
                    self)._prepare_account_move_line(
                        move, qty, cost,
                        credit_account_id,
                        debit_account_id,
                        context=context
                        )

        # Add project in debit line
        if move.account_analytic_id:
            res[0][2].update({
                'project_id': move.project_id.id,
            })
            res[1][2].update({
                'project_id': move.project_id.id,
            })
        return res
