# -*- coding: utf-8 -*-
#    Copyright 2015 Matmoz d.o.o. (Matjaž Mozetič)
#    Copyright 2015 Eficent (Jordi Ballester Alomar)
#    Copyright 2017 Luxim d.o.o. (Matjaž Mozetič)
#    License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

import time
import openerp.addons.decimal_precision as dp
from openerp import api, fields, models
from openerp.tools.translate import _
from openerp.exceptions import Warning as UserError


class BillingPlanLine(models.Model):
    _name = 'analytic.billing.plan.line'
    _description = "Billing Plan Lines"
    _inherit = ['mail.thread', 'ir.needaction_mixin']
    _inherits = {'account.analytic.line.plan': "analytic_line_plan_id"}

    @api.multi
    def _compute_active_order(self):
        for rec in self:
            for order_line in rec.order_line_ids:
                if order_line.state and order_line.state != 'cancel':
                    rec.has_active_order = bool(rec.order_line_ids)

    unit_price = fields.Float(
        string='Sale Price',
        groups='project.group_project_manager',
        digits=dp.get_precision('Sale Price'),
        oldname='price_unit'
    )
    customer_id = fields.Many2one(
        comodel_name='res.partner',
        string='Partner',
        related='account_id.partner_id',
        readonly=True
    )
    analytic_line_plan_id = fields.Many2one(
        comodel_name='account.analytic.line.plan',
        string='Planning lines',
        ondelete="cascade",
        required=True
    )
    order_line_ids = fields.Many2many(
        comodel_name='sale.order.line',
        relation='analytic_billing_plan_order_line_rel',
        column1='order_line_id',
        column2='analytic_billing_plan_line_id'
    )
    has_active_order = fields.Boolean(
        compute='_compute_active_order',
        string='Billing request',
        help='Indicates that this billing plan line '
             'contains at least one non-cancelled billing request.'
    )
    resource_ids = fields.One2many(
        comodel_name='analytic.resource.plan.line',
        inverse_name='deliverable_id',
        string='Resource Lines',
        copy=True,
    )
    # TODO: add reference to gap lines
    # the idea is, that the deliverable manager could have a list of user
    # user stories on the deliverable form to follow completion of assigned
    # tasks that he encoded in the resources; the deliverable becomes s
    # sprint

    # todo_ids = fields.One2many(
    #     comodel_name="change.gap.analysis",
    #     inverse_name="deliverable_id",
    #     string="User Stories"
    # )

    @api.onchange('unit_amount')
    def on_change_unit_amount(self):
        if self.unit_amount:
            self.amount = self.unit_price * self.unit_amount

    @api.onchange('unit_price')
    def on_change_unit_price(self):
        if self.unit_price:
            self.amount = self.unit_price * self.unit_amount

    @api.onchange('product_id')
    def on_change_product_id(self):
        if self.product_id:
            if self.product_id.description_sale:
                self.name = self.product_id.description_sale
            if not self.product_id.description_sale:
                self.name = self.product_id.name
            self.product_uom_id = (
                self.product_id.uom_id and
                self.product_id.uom_id.id or
                False
            )
            self.unit_price = self.product_id.list_price
            self.journal_id = (
                self.product_id.revenue_analytic_plan_journal_id and
                self.product_id.revenue_analytic_plan_journal_id.id or
                False
            )

    @api.onchange('account_id')
    def on_change_account_id(self):
        if self.account_id:
            if self.account_id.date:
                self.date = self.account_id.date
            if self.account_id.partner_id:
                self.partner_id = self.account_id.partner_id.id
            if self.account_id.company_id.currency_id:
                self.currency_id = self.account_id.company_id.currency_id.id
                self.amount = self.unit_price * self.unit_amount

    @api.multi
    @api.depends('unit_price', 'unit_amount')
    def _total_price(self):
        self.amount = self.unit_price * self.unit_amount

    @api.multi
    def copy(self, default=None):
        self.ensure_one()
        if default is None:
            default = {}
        default['parent_id'] = False
        default['analytic_line_plan_ids'] = []
        res = super(BillingPlanLine, self).copy(default)
        return res

    @api.multi
    def unlink(self):
        for line in self:
            if line.analytic_line_plan_ids:
                raise UserError(
                    _(
                        'You cannot delete a record that refers to '
                        'analytic plan lines!'
                    )
                )
        return super(BillingPlanLine, self).unlink()

class ResourcePlanLine(models.Model):

    _inherit = 'analytic.resource.plan.line'

    deliverable_id = fields.Many2one(
        comodel_name='analytic.billing.plan.line',
        string='Deliverable',
        ondelete='cascade'
    )

    @api.onchange('deliverable_id')
    def on_change_deliverable_id(self):
        if self.deliverable_id:
            self.account_id = self.deliverable_id.account_id
