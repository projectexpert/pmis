# -*- coding: utf-8 -*-
# Copyright 2017 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models
import odoo.addons.decimal_precision as dp
from odoo import SUPERUSER_ID


class AnalyticResourcePlanLine(models.Model):

    _inherit = 'analytic.resource.plan.line'

    @api.multi
    def _compute_qty_available(self):
        """ Finds the incoming and outgoing quantity of product on the
        for that analytic account and the location defaulted in the analytic
        account.
        @return: Dictionary of values
        """
        product_obj = self.env['product.product']
        for line in self:
            if line.product_id.type == 'service':
                continue
            location_id = (
                line.account_id.location_id and
                line.account_id.location_id.id or False
            )
            for f in field_names:
                if line.account_id.use_reserved_stock:
                    c.update({'analytic_account_id': line.account_id.id})
                if location_id:
                    c.update({'location_id': location_id})
                if f == 'qty_available':
                    c.update(
                        {
                            'states': ('done',),
                            'what': ('in', 'out')
                        }
                    )
                if f == 'virtual_available':
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
                if f == 'incoming_qty':
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
                if f == 'incoming_done_qty':
                    c.update(
                        {
                            'states': ('done',),
                            'what': ('in',)
                        }
                    )
                if f == 'outgoing_qty':
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
                if f == 'outgoing_done_qty':
                    c.update(
                        {'states': ('done',), 'what': ('out',)}
                    )

                stock = product_obj.get_product_available(
                    cr, uid, [line.product_id.id], context=c
                )
                res[line.id][f] = stock.get(line.product_id.id, 0.0)
        return res

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
        compute=_compute_qty_available,
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
        compute=_compute_qty_available,
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
