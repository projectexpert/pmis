# -*- coding: utf-8 -*-
# © 2017 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openerp import _, api, fields, models
from openerp.tools.misc import DEFAULT_SERVER_DATETIME_FORMAT
from openerp.exceptions import Warning as UserError
import openerp.addons.decimal_precision as dp
import time


class AnalyticResourcePlanLine(models.Model):

    _inherit = 'analytic.resource.plan.line'

    @api.multi
    def _get_product_available(self, location):

        """ Finds the incoming and outgoing quantity of product on the
        for that analytic account and the location defaulted in the analytic
        account.
        @return: Dictionary of values
        """
        res = {}

        for line in self:
            if line.product_id.type == 'service':
                continue
            c = self.env.context.copy()
            c.update({'states': ('done',), 'what': ('in', 'out'),
                      'location': location})
            stock = line.with_context(c).product_id._product_available()
            res[line.id] = stock.get(line.product_id.id, 0.0)
        return res

    @api.multi
    def _compute_qty_fetched(self):
        qty=0.0
        for line in self:
            for picking in line.picking_ids.filtered(
                    lambda p: p.state != 'cancel'):
                for move in picking.move_lines:
                    qty += move.product_uom_qty
        self.qty_fetched = qty

    @api.multi
    def _compute_qty_left(self):
        qty=0.0
        for line in self:
            for picking in line.picking_ids.filtered(
                    lambda p: p.state != 'cancel'):
                for move in picking.move_lines:
                    qty += move.product_uom_qty
        self.qty_left = self.unit_amount - qty
        return self.qty_left

    picking_ids = fields.One2many(
            'stock.picking',
            'analytic_resource_plan_line_id',
            'Pickings', readonly=True)

    qty_fetched = fields.Float(
        string='Fetched Quantity',
        digits=dp.get_precision('Product Unit of Measure'),
        compute=_compute_qty_fetched)
    qty_left = fields.Float(
        string='Quantity left',
        default=lambda self: self.unit_amount,
        compute=_compute_qty_left,
        digits=dp.get_precision('Product Unit of Measure'))

    @api.model
    def get_picking_type(self, dest_loc):
        domain = [('default_location_dest_id', '=', dest_loc.id)]
        picking_type = self.env['stock.picking.type'].search(domain)
        if not picking_type:
            raise UserError(_('Please define a picking type for the'
                              ' destination the project location'))
        return picking_type

    @api.multi
    def _prepare_picking_vals(self, warehouse, src_location):
        self.ensure_one()
        dest_location = self.account_id.location_id
        return {
            'origin': self.name,
            'type': 'internal',
            'move_type': 'one',  # direct
            'state': 'draft',
            'picking_type_id': self.get_picking_type(dest_location).id,
            'date': time.strftime(DEFAULT_SERVER_DATETIME_FORMAT),
            'partner_id': self.account_id.partner_id.id,
            'invoice_state': "none",
            'company_id': self.account_id.company_id.id,
            'location_id': src_location.id,
            'warehouse_id': warehouse.id,
            'location_dest_id': dest_location.id,
            'analytic_resource_plan_line_id': self.id,
            'note': 'Resource Plan Line %s %s' % (
                self.account_id.id, self.name),
        }

    @api.multi
    def _prepare_move_vals(self, qty_available, picking_id, scr_location):
        self.ensure_one()
        product_qty = self.unit_amount
        if self.unit_amount > qty_available:
            product_qty = qty_available
        return {
            'name': self.product_id.name_template,
            'priority': '0',
            'date': time.strftime(DEFAULT_SERVER_DATETIME_FORMAT),
            'date_expected': time.strftime(DEFAULT_SERVER_DATETIME_FORMAT),
            'product_id': self.product_id.id,
            'product_uom_qty': qty_available,
            'product_uom': self.product_uom_id.id,
            'partner_id': self.account_id.partner_id.id,
            'picking_id': picking_id.id,
            'state': 'draft',
            'analytic_account_id': self.account_id.id,
            'price_unit': self.product_id.price,
            'company_id': self.account_id.company_id.id,
            'location_id': scr_location.id,
            'location_dest_id': self.account_id.location_id.id,
            'note': 'Move for project',
        }

    @api.multi
    def action_button_draft(self):
        res = super(AnalyticResourcePlanLine, self).action_button_draft()
        for line in self:
            if line.picking_ids:
                for picking in line.picking_ids:
                    picking.action_cancel()
        return res

    @api.multi
    def action_button_confirm(self):
        for line in self:
            if not line.account_id.location_id:
                raise UserError(
                    _('Could not fetch stock. You have to set a location for'
                      ' the project'))
            company_id = line.account_id.company_id.id
            warehouses = self.env['stock.warehouse'].search(
                [('company_id', '=', company_id)])
            qty_fetched = line.qty_fetched
            for warehouse in warehouses:
                if warehouse.lot_stock_id:
                    for location_id in \
                            warehouse.lot_stock_id._get_sublocations():
                        if qty_fetched < line.unit_amount:
                            location = self.env['stock.location'].\
                                browse(location_id)
                            qty_available = self._get_product_available(
                                location.id)[line.id]['qty_available']
                            if qty_available > 0:
                                picking = self._prepare_picking_vals(
                                    warehouse, location)
                                picking_id = self.env['stock.picking'].create(
                                    picking)
                                move_vals = line._prepare_move_vals(
                                    qty_available, picking_id, location)
                                move = self.env['stock.move'].create(move_vals)
                                qty_fetched += move.product_uom_qty
        return super(AnalyticResourcePlanLine, self).action_button_confirm()

    @api.multi
    def unlink(self):
        for line in self:
            if line.picking_ids:
                raise UserError(
                    _('You cannot delete a record that refers to a picking'))
        return super(AnalyticResourcePlanLine, self).unlink()
