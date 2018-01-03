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

    @api.model
    def _get_rpls_from_purchase_requests(self):
        rpl_ids = []
        for request in self.env['purchase.request']:
            for request_line in request.line_ids:
                for rpl in request_line.analytic_resource_plan_lines:
                    rpl_ids.append(rpl.id)
        return list(set(rpl_ids))

    @api.model
    def _get_rpls_from_purchase_request_lines(self):
        rpl_ids = []
        for request_line in self.env['purchase.request.line']:
            for rpl in request_line.analytic_resource_plan_lines:
                rpl_ids.append(rpl.id)

        return list(set(rpl_ids))

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

    # qty_fetched = fields.Float(
    #     string='Fetched Quantity',
    #     digits=dp.get_precision('Product Unit of Measure'),
    #     compute=_compute_qty_fetched)

    # qty_left = fields.Float(
    #     string='Quantity left',
    #     default=lambda self: self.unit_amount,
    #     compute=_compute_qty_left,
    #     digits=dp.get_precision('Product Unit of Measure'))

    @api.multi
    def unlink(self):
        for line in self:
            if line.purchase_request_lines:
                raise ValidationError(
                    _('You cannot delete a record that refers to purchase '
                      'purchase request lines!'))
        return super(AnalyticResourcePlanLine, self).unlink()
