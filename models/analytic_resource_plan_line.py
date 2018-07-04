# -*- coding: utf-8 -*-
# Copyright 2017 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models
import odoo.addons.decimal_precision as dp


class AnalyticResourcePlanLine(models.Model):

    _inherit = 'analytic.resource.plan.line'

    @api.multi
    def _compute_quantities(self):
        for line in self:
            stock = line.with_context(
                analytic_account_id=line.account_id.id).product_id.\
                _product_available()
            if stock.get(line.product_id.id, False):
                line.incoming_qty = stock[line.product_id.id]['incoming_qty']
                line.outgoing_qty = stock[line.product_id.id]['outgoing_qty']
                line.virtual_available = \
                    stock[line.product_id.id]['virtual_available']
                line.qty_available = stock[line.product_id.id]['qty_available']
            else:
                line.incoming_qty = 0.0
                line.outgoing_qty = 0.0
                line.virtual_available = 0.0
                line.qty_available = 0.0

    @api.multi
    def _compute_done_quantities(self):
        for line in self:
            stock = line.with_context(
                analytic_account_id_out=line.account_id.id).product_id.\
                _product_available()
            if stock.get(line.product_id.id, False):
                #  available in customer means done
                line.outgoing_done_qty = (
                    stock[line.product_id.id]['qty_available'])
            else:
                line.outgoing_done_qty = 0.0
            line.incoming_done_qty = (line.qty_available - line.outgoing_qty
                                      - line.outgoing_done_qty)

    qty_available = fields.Float(
        string='Qty Available',
        digits=dp.get_precision('Product Unit of Measure'),
        compute='_compute_quantities',
        help="Current quantity of products. "
             "In a context with a single Stock Location, this includes "
             "goods stored at this Location, or any of its children. "
             "In a context with a single Warehouse, this includes "
             "goods stored in the Stock Location of this Warehouse, "
             "or any of its children. "
             "In a context with a single Shop, this includes goods "
             "stored in the Stock Location of the Warehouse of this Shop, "
             "or any of its children. "
             "Otherwise, this includes goods stored in any Stock Location "
             "with 'internal' type."
    )
    virtual_available = fields.Float(
        string='Virtually available',
        compute='_compute_quantities',
        digits=dp.get_precision('Product Unit of Measure'),
        help="Forecast quantity (computed as Quantity On Hand "
             "- Outgoing + Incoming) "
             "In a context with a single Stock Location, this includes "
             "goods stored in this location, or any of its children. "
             "In a context with a single Warehouse, this includes "
             "goods stored in the Stock Location of this Warehouse, "
             "or any of its children. "
             "In a context with a single Shop, this includes goods "
             "stored in the Stock Location of the Warehouse of this Shop, "
             "or any of its children. "
             "Otherwise, this includes goods stored in any Stock Location "
             "with 'internal' type."
    )
    incoming_qty = fields.Float(
        string='Qty Incoming',
        digits=dp.get_precision('Product Unit of Measure'),
        compute='_compute_quantities',
        help="Quantity of products that are planned to arrive. "
             "In a context with a single Stock Location, this includes "
             "goods arriving to this Location, or any of its children. "
             "In a context with a single Warehouse, this includes "
             "goods arriving to the Stock Location of this Warehouse, or "
             "any of its children. "
             "In a context with a single Shop, this includes goods "
             "arriving to the Stock Location of the Warehouse of this "
             "Shop, or any of its children. "
             "Otherwise, this includes goods arriving to any Stock "
             "Location with 'internal' type."
    )
    outgoing_qty = fields.Float(
        string='Virtually available',
        default=lambda self: self.unit_amount,
        compute='_compute_quantities',
        digits=dp.get_precision('Product Unit of Measure'),
        help="Quantity of products that are planned to leave. "
             "In a context with a single Stock Location, this includes "
             "goods leaving this Location, or any of its children. "
             "In a context with a single Warehouse, this includes "
             "goods leaving the Stock Location of this Warehouse, or "
             "any of its children. "
             "In a context with a single Shop, this includes goods "
             "leaving the Stock Location of the Warehouse of this "
             "Shop, or any of its children. "
             "Otherwise, this includes goods leaving any Stock "
             "Location with 'internal' type."
    )

    incoming_done_qty = fields.Float(
        string='Qty Incoming Done',
        digits=dp.get_precision('Product Unit of Measure'),
        compute='_compute_done_quantities',
        help="Quantity of products that have been produced or have "
             "arrived."
    )
    outgoing_done_qty = fields.Float(
        string='Qty Outgoing Done',
        default=lambda self: self.unit_amount,
        compute='_compute_done_quantities',
        digits=dp.get_precision('Product Unit of Measure'),
        help="Quantity of products that have been consumed or delivered."
    )
