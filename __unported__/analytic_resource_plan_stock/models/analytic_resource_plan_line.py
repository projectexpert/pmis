# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2015 Eficent (<http://www.eficent.com/>)
#              <contact@eficent.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
from openerp.osv import fields, orm
import openerp.addons.decimal_precision as dp
from openerp import SUPERUSER_ID


class AnalyticResourcePlanLine(orm.Model):

    _inherit = 'analytic.resource.plan.line'

    def _product_available(
        self, cr, uid, ids, field_names=None, arg=False, context=None
    ):
        """ Finds the incoming and outgoing quantity of product on the
        for that analytic account and the location defaulted in the analytic
        account.
        @return: Dictionary of values
        """
        if context is None:
            context = {}
        res = {}
        product_obj = self.pool['product.product']
        for id in ids:
            res[id] = {}.fromkeys(field_names, 0.0)

        for line in self.browse(cr, SUPERUSER_ID, ids, context=context):
            if line.product_id.type == 'service':
                continue
            location_id = (
                line.account_id.location_id and
                line.account_id.location_id.id or False
            )
            if not field_names:
                field_names = []
            for f in field_names:
                c = context.copy()
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

    _columns = {
        'qty_available': fields.function(
            _product_available, multi='qty_available',
            type='float',
            digits_compute=dp.get_precision('Product Unit of Measure'),
            string='Quantity On Hand',
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
                 "with 'internal' type."),
        'virtual_available': fields.function(
            _product_available, multi='qty_available',
            type='float',
            digits_compute=dp.get_precision('Product Unit of Measure'),
            string='Forecasted Quantity',
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
                 "with 'internal' type."),
        'incoming_qty': fields.function(
            _product_available, multi='qty_available',
            type='float',
            digits_compute=dp.get_precision('Product Unit of Measure'),
            string='Incoming',
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
                 "Location with 'internal' type."),
        'outgoing_qty': fields.function(
            _product_available, multi='qty_available',
            type='float',
            digits_compute=dp.get_precision('Product Unit of Measure'),
            string='Outgoing',
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
                 "Location with 'internal' type."),
        'incoming_done_qty': fields.function(
            _product_available, multi='qty_available',
            type='float',
            digits_compute=dp.get_precision('Product Unit of Measure'),
            string='Received/Produced',
            help="Quantity of products that have been produced or have "
                 "arrived."),
        'outgoing_done_qty': fields.function(
            _product_available, multi='qty_available',
            type='float',
            digits_compute=dp.get_precision('Product Unit of Measure'),
            string='Delivered/Consumed',
            help="Quantity of products that have been consumed or delivered."),
    }
