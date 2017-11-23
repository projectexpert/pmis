# -*- coding: utf-8 -*-
# Copyright 2017 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models
import odoo.addons.decimal_precision as dp


class AnalyticResourcePlanLine(models.Model):

    _inherit = 'analytic.resource.plan.line'

    @api.multi
    def _compute_qty_available(self):
        """ Finds the incoming and outgoing quantity of product on the
        for that analytic account and the location defaulted in the analytic
        account.
        """
        for line in self:
            if line.product_id.type == 'service':
                continue
            c = self.env.context.copy()
            location_id = (
                line.account_id.location_id and
                line.account_id.location_id.id or False
            )
            c.update({'analytic_account_id': line.account_id.id})
            if location_id:
                c.update({'location_id': location_id})
            c.update(
                {
                    'states': ('done',),
                    'what': ('in', 'out')
                }
            )
            stock = line.with_context(c).product_id._product_available()
            line.qty_available = stock.get('qty_available', 0.0)
        return True

    def _compute_virtual_available(self):
        for line in self:
            if line.product_id.type == 'service':
                continue
            c = self.env.context.copy()
            location_id = (
                line.account_id.location_id and
                line.account_id.location_id.id or False
            )
            c.update({'analytic_account_id': line.account_id.id})
            if location_id:
                c.update({'location_id': location_id})
            c.update(
                {
                    'states': (
                        'confirmed',
                        'waiting',
                        'assigned',
                        'done'
                    ),
                    'what': ('in', 'out')
                }
            )
            stock = line.with_context(c).product_id._product_available()
            line.virtual_available = stock.get('virtual_available', 0.0)
        return True

    def _compute_incoming_qty(self):
        for line in self:
            if line.product_id.type == 'service':
                continue
            c = self.env.context.copy()
            location_id = (
                line.account_id.location_id and
                line.account_id.location_id.id or False
            )
            c.update({'analytic_account_id': line.account_id.id})
            if location_id:
                c.update({'location_id': location_id})
            c.update(
                {
                    'states': (
                        'confirmed',
                        'waiting',
                        'assigned'
                    ),
                    'what': ('in',)
                }
            )
            stock = line.with_context(c).product_id._product_available()
            line.incoming_qty = stock.get('incoming_qty', 0.0)
        return True

    def _compute_outgoing_qty(self):
        for line in self:
            if line.product_id.type == 'service':
                continue
            c = self.env.context.copy()
            location_id = (
                line.account_id.location_id and
                line.account_id.location_id.id or False
            )
            c.update({'analytic_account_id': line.account_id.id})
            if location_id:
                c.update({'location_id': location_id})
            c.update(
                {
                    'states': (
                        'confirmed',
                        'waiting',
                        'assigned'
                    ),
                    'what': ('out',)
                }
            )
            stock = line.with_context(c).product_id._product_available()
            line.outgoing_qty = stock.get('outgoing_qty', 0.0)
        return True

    def _compute_incoming_done_qty(self):
        for line in self:
            if line.product_id.type == 'service':
                continue
            c = self.env.context.copy()
            location_id = (
                line.account_id.location_id and
                line.account_id.location_id.id or False
            )
            c.update({'analytic_account_id': line.account_id.id})
            if location_id:
                c.update({'location_id': location_id})
            c.update(
                {
                    'states': ('done',),
                    'what': ('in',)
                }
            )
            stock = line.with_context(c).product_id._product_available()
            line.incoming_done_qty = stock.get('incoming_qty', 0.0)
        return True

    def _compute_outgoing_done_qty(self):
        for line in self:
            if line.product_id.type == 'service':
                continue
            c = self.env.context.copy()
            location_id = (
                line.account_id.location_id and
                line.account_id.location_id.id or False
            )
            c.update({'analytic_account_id': line.account_id.id})
            if location_id:
                c.update({'location_id': location_id})
            c.update(
                {
                    'states': ('done',),
                    'what': ('out',)
                }
            )
            stock = line.with_context(c).product_id._product_available()
            line.outgoing_done_qty = stock.get('outgoing_qty', 0.0)
        return True

    qty_available = fields.Float(
        string='Quantity Available',
        digits=dp.get_precision('Product Unit of Measure'),
        compute=_compute_qty_available,
        help="Current quantity of products.\n"
             "In a context with a single Stock Location, this includes "
             "goods stored at this Location, or any of its children.\n"
             "In a context with a single Warehouse, this includes "
             "goods stored in the Stock Location of this Warehouse, "
             "or any of its children.\n"
             "In a context with a single Shop, this includes goods "
             "stored in the Stock Location of the Warehouse of this Shop, "
             "or any of its children.\n"
             "Otherwise, this includes goods stored in any Stock Location "
             "with 'internal' type."
    )
    virtual_available = fields.Float(
        string='Virtually available',
        default=lambda self: self.unit_amount,
        compute=_compute_virtual_available,
        digits=dp.get_precision('Product Unit of Measure'),
        help="Forecast quantity (computed as Quantity On Hand "
             "- Outgoing + Incoming)\n"
             "In a context with a single Stock Location, this includes "
             "goods stored in this location, or any of its children.\n"
             "In a context with a single Warehouse, this includes "
             "goods stored in the Stock Location of this Warehouse, "
             "or any of its children.\n"
             "In a context with a single Shop, this includes goods "
             "stored in the Stock Location of the Warehouse of this Shop, "
             "or any of its children.\n"
             "Otherwise, this includes goods stored in any Stock Location "
             "with 'internal' type."
    )
    incoming_qty = fields.Float(
        string='Quantity Incoming',
        digits=dp.get_precision('Product Unit of Measure'),
        compute=_compute_incoming_qty,
        help="Quantity of products that are planned to arrive.\n"
             "In a context with a single Stock Location, this includes "
             "goods arriving to this Location, or any of its children.\n"
             "In a context with a single Warehouse, this includes "
             "goods arriving to the Stock Location of this Warehouse, or "
             "any of its children.\n"
             "In a context with a single Shop, this includes goods "
             "arriving to the Stock Location of the Warehouse of this "
             "Shop, or any of its children.\n"
             "Otherwise, this includes goods arriving to any Stock "
             "Location with 'internal' type."
    )
    outgoing_qty = fields.Float(
        string='Virtually available',
        default=lambda self: self.unit_amount,
        compute=_compute_qty_available,
        digits=dp.get_precision('Product Unit of Measure'),
        help="Quantity of products that are planned to leave.\n"
             "In a context with a single Stock Location, this includes "
             "goods leaving this Location, or any of its children.\n"
             "In a context with a single Warehouse, this includes "
             "goods leaving the Stock Location of this Warehouse, or "
             "any of its children.\n"
             "In a context with a single Shop, this includes goods "
             "leaving the Stock Location of the Warehouse of this "
             "Shop, or any of its children.\n"
             "Otherwise, this includes goods leaving any Stock "
             "Location with 'internal' type."
    )

    incoming_done_qty = fields.Float(
        string='Quantity Incoming Done',
        digits=dp.get_precision('Product Unit of Measure'),
        compute=_compute_qty_available,
        help="Quantity of products that have been produced or have "
             "arrived."
    )
    outgoing_done_qty = fields.Float(
        string='Quantity Outgoing Done',
        default=lambda self: self.unit_amount,
        compute=_compute_qty_available,
        digits=dp.get_precision('Product Unit of Measure'),
        help="Quantity of products that have been consumed or delivered."
    )
