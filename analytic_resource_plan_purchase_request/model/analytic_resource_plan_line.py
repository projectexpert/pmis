# -*- coding: utf-8 -*-
#    Copyright 2017 Matmoz d.o.o. (Matjaž Mozetič)
#    Copyright 2017 Eficent (Jordi Ballester Alomar)
#    Copyright 2017 Luxim d.o.o. (Matjaž Mozetič)
#    License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openerp import _, api, fields, models
from openerp.addons.decimal_precision import decimal_precision as dp
from openerp.exceptions import ValidationError


_REQUEST_STATE = [
    ('none', 'No Request'),
    ('draft', 'Draft'),
    ('to_approve', 'To be approved'),
    ('approved', 'Approved'),
    ('rejected', 'Rejected')
]


class AnalyticResourcePlanLine(models.Model):

    _inherit = 'analytic.resource.plan.line'

    @api.multi
    def _requested_qty(self):
        for line in self:
            requested_qty = 0.0
            for purchase_line in line.purchase_request_lines:
                if purchase_line.request_id.state != 'rejected':
                    requested_qty += purchase_line.product_qty
            line.requested_qty = requested_qty
        return True

    @api.multi
    def _compute_qty_fetched(self):
        qty = 0.0
        for line in self:
            for picking in line.picking_ids.filtered(
                    lambda p: p.state != 'cancel'):
                for move in picking.move_lines:
                    qty += move.product_uom_qty + self.requested_qty
        self.qty_fetched = qty

    @api.multi
    def _compute_qty_left(self):
        qty = 0.0
        for line in self:
            for picking in line.picking_ids.filtered(
                    lambda p: p.state != 'cancel'):
                for move in picking.move_lines:
                    qty += move.product_uom_qty
        self.qty_left = self.unit_amount - qty - self.requested_qty
        return self.qty_left

    @api.model
    def _get_request_state(self):
            for line in self:
                self.request_state = 'none'
                if any([pr_line.request_id.state == 'approved' for pr_line in
                        line.purchase_request_lines]):
                    self.request_state = 'approved'
                elif all([pr_line.request_id.state == 'cancel' for pr_line in
                          line.purchase_request_lines]):
                    self.request_state = 'cancel'
                elif all([po_line.request_id.state in ('to_approve', 'cancel')
                          for po_line in line.purchase_request_lines]):
                    self.request_state = 'to_approve'
                elif any([po_line.request_id.state == 'approved' for po_line in
                          line.purchase_request_lines]):
                    self.request_state = 'approved'
                elif all([po_line.request_id.state in ('draft', 'cancel')
                          for po_line in line.purchase_request_lines]):
                    self.request_state = 'draft'
            return True

    requested_qty = fields.Float(
        compute=_requested_qty,
        string='Requested quantity',
        digits=dp.get_precision('Product Unit of Measure'),
        readonly=True)

    request_state = fields.Selection(
        compute=_get_request_state, string='Request status',
        selection=_REQUEST_STATE,
        store=True,
        default=None,
    )
    purchase_request_lines = fields.Many2many(
        'purchase.request.line',
        copy=False,
        string='Purchase Request Lines',
        readonly=True)

    qty_fetched = fields.Float(
        string='Fetched Quantity',
        digits=dp.get_precision('Product Unit of Measure'),
        compute=_compute_qty_fetched)

    qty_left = fields.Float(
        string='Quantity left',
        default=lambda self: self.unit_amount,
        compute=_compute_qty_left,
        digits=dp.get_precision('Product Unit of Measure'))

    @api.multi
    def unlink(self):
        for line in self:
            if line.purchase_request_lines:
                raise ValidationError(
                    _('You cannot delete a record that refers to purchase '
                      'purchase request lines!'))
        return super(AnalyticResourcePlanLine, self).unlink()

    @api.multi
    def action_button_draft(self):
        res = super(AnalyticResourcePlanLine, self).action_button_draft()
        for line in self:
            for request_line in line.purchase_request_lines:
                request_line.request_id.button_rejected()
        return res

    @api.multi
    def action_button_confirm(self):
        res = super(AnalyticResourcePlanLine, self).action_button_confirm()
        if self.qty_left > 0.0:
            self._make_purchase_request()
        return res

    @api.model
    def _prepare_purchase_request(self, line, company_id):
        data = {
            'company_id': company_id,
            'origin': line.name,
            'description': line.product_id.name_template,
        }
        return data

    def _prepare_purchase_request_line(self, pr_id, line, qty):
        return {
            'request_id': pr_id.id,
            'name': line.product_id.name,
            'product_qty': qty,
            'product_id': line.product_id.id,
            'product_uom_id': line.product_uom_id.id,
            'date_required': line.date or False,
            'analytic_account_id': line.account_id.id,
            'analytic_resource_plan_lines': [(4, line.id)]
        }

    @api.multi
    def _make_purchase_request(self):
        res = []
        request_obj = self.env['purchase.request']
        request_line_obj = self.env['purchase.request.line']
        company_id = False
        warehouse_id = False
        request_id = False
        for line in self.filtered(lambda t: t.qty_left > 0.0):
            if line.state != 'confirm':
                raise ValidationError(
                    _('All resource plan lines must be  '
                      'confirmed.'))
            line_company_id = line.account_id.company_id.id or False
            if company_id is not False \
                    and line_company_id != company_id:
                raise ValidationError(
                    _('You have to select lines '
                      'from the same company.'))
            else:
                company_id = line_company_id
            line_warehouse_id = (
                self.env['stock.location'].get_warehouse(
                    line.account_id.location_id
                ) or False
            )
            if warehouse_id is not False \
                    and line_warehouse_id != warehouse_id:
                raise ValidationError(
                    _('You have to select lines '
                      'from the same warehouse.'))
            else:
                warehouse_id = line_warehouse_id

            if request_id is False:
                request_data = self._prepare_purchase_request(
                    line, company_id)
                request_id = request_obj.create(request_data)
            request_line_data = self._prepare_purchase_request_line(
                request_id, line, line.qty_left)
            request_line_id = request_line_obj.create(
                request_line_data)
            values = {
                'purchase_request_lines': [(4, request_line_id.id)]
            }
            line.write(values)
            # todo: fix this
            # project_manager_id = \
            #     line.account_id.user_id.partner_id or False
            # if project_manager_id:
            #     message_follower_ids = [x.id for x in
            #                             request_id.message_follower_ids]
            #     if project_manager_id not in message_follower_ids:
            #         request_id.write({
            #             'message_follower_ids': (4, project_manager_id)})
            res.append(request_line_id)

        return {
            'domain': "[('id','in', [" + ','.join(map(str, res)) + "])]",
            'name': _('Purchase Request Lines'),
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'purchase.request.line',
            'view_id': False,
            'context': False,
            'type': 'ir.actions.act_window'
        }