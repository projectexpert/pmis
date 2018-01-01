# -*- coding: utf-8 -*-
# © 2015-17 Eficent Business and IT Consulting Services S.L.
#  - Jordi Ballester Alomar
# © 2015-17 MATMOZ d.o.o.
#  - Matjaž Mozetič
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openerp import models, api


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    @api.model
    def _prepare_order_line_move(self, order, order_line, picking_id,
                                 group_id):
        res = super(PurchaseOrder, self)._prepare_order_line_move(
            order, order_line, picking_id, group_id
        )
        for vals in res:
            vals.update({'analytic_account_id': (
                order_line.account_analytic_id.id)}
            )
        # res['analytic_account_id'] = order_line.account_analytic_id.id

        return res

# from openerp import api, fields, models
#
#
# class PurchaseOrder(models.Model):
#
#     _inherit = "purchase.order"
#
#     @api.multi
#     def _create_stock_moves(self, picking):
#         """
#         Warning this method overwrite the standard behaviour to update the
#         move dict
#         """
#         moves = self.env['stock.move']
#         done = self.env['stock.move'].browse()
#         for line in self:
#             price_unit = line._get_stock_move_price_unit()
#
#             template = {
#                 'name': line.name or '',
#                 'product_id': line.product_id.id,
#                 'product_uom': line.product_uom.id,
#                 'date': line.order_id.date_order,
#                 'date_expected': line.date_planned,
#                 'location_id': (
#                     line.order_id.partner_id.property_stock_supplier.id),
#                 'location_dest_id': line.order_id._get_destination_location(),
#                 'picking_id': picking.id,
#                 'partner_id': line.order_id.dest_address_id.id,
#                 'move_dest_id': False,
#                 'state': 'draft',
#                 'purchase_line_id': line.id,
#                 'company_id': line.order_id.company_id.id,
#                 'price_unit': price_unit,
#                 'picking_type_id': line.order_id.picking_type_id.id,
#                 'group_id': line.order_id.group_id.id,
#                 'procurement_id': False,
#                 'origin': line.order_id.name,
#                 'analytic_account_id': line.analytic_account_id,
#                 'route_ids': (
#                         line.order_id.picking_type_id.warehouse_id and
#                         [(6, 0, [
#                             x.id for x in
#                             line.order_id.picking_type_id.warehouse_id.route_ids
#                         ])] or []),
#                 'warehouse_id':line.order_id.picking_type_id.warehouse_id.id,
#             }
#
#             # Fullfill all related procurements with this po line
#             diff_quantity = line.product_qty
#             for procurement in line.procurement_ids:
#                 procurement_qty = procurement.product_uom._compute_qty_obj(
#                     procurement.product_uom,
#                     procurement.product_qty,
#                     line.product_uom
#                 )
#                 tmp = template.copy()
#                 tmp.update({
#                     'product_uom_qty': min(procurement_qty, diff_quantity),
#                     # move destination is same as procurement destination
#                     'move_dest_id': procurement.move_dest_id.id,
#                     'procurement_id': procurement.id,
#                     'propagate': procurement.rule_id.propagate,
#                 })
#                 done += moves.create(tmp)
#                 diff_quantity -= min(procurement_qty, diff_quantity)
#             if float_compare(
#                     diff_quantity,
#                     0.0,
#                     precision_rounding=line.product_uom.rounding
#             ) > 0:
#                 template['product_uom_qty'] = diff_quantity
#                 done += moves.create(template)
#         return done
