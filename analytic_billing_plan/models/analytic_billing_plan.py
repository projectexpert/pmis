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
    _description = "Deliverable Lines"
    _inherit = ['mail.thread', 'ir.needaction_mixin']
    _inherits = {'account.analytic.line.plan': "analytic_line_plan_id"}

    @api.multi
    def _compute_active_order(self):
        for rec in self:
            for order_line in rec.order_line_ids:
                if order_line.state and order_line.state != 'cancel':
                    rec.has_active_order = bool(rec.order_line_ids)

    @api.multi
    @api.depends('version_id', 'active_account_version', 'account_id')
    def _compute_is_active(self):
        for res in self:
            if res.version_id == res.active_account_version:
                res.is_active = True
            else:
                res.is_active = False

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
    task_margin = fields.Float(
        string='Work Price Margin (%)',
        help='Sale Margin for work in %',
        groups='project.group_project_manager',
        default='66',
        required=True
    )
    procurement_margin = fields.Float(
        string='Material Price Margin (%)',
        help='Sale Margin for materials in %',
        groups='project.group_project_manager',
        default='66',
        required=True
    )
    target_revenue = fields.Float(
        string='Target budget',
        help='Target budget computed from costs and wanted margin.',
        groups='project.group_project_manager',
        compute='_compute_target_revenue'
    )
    resource_task_total = fields.Float(
        compute='_compute_resource_task_total',
        string='Total tasks',
        store=True
    )
    resource_procurement_total = fields.Float(
        compute='_compute_resource_procurement_total',
        string='Total procurement',
        store=True
    )
    delivered_task = fields.Float(
        compute='_compute_sale_task_total',
        string='Total work',
        help='Total tasks sale price',
        store=True
    )
    delivered_material = fields.Float(
        compute='_compute_sale_procurement_total',
        string='Total material',
        help='Total materials sale price',
        store=True
    )
    wanted_price_unit = fields.Float(
        compute='_compute_wanted_price_unit',
        string='Budget/Unit',
        help='Proposed sale price per UoM'
    )
    active_account_version = fields.Many2one(
        related='account_id.active_analytic_planning_version'
    )
    is_active = fields.Boolean(
        string="Active version",
        readonly=True,
        compute='_compute_is_active',
        store=True
    )

    @api.multi
    @api.depends('resource_ids', 'resource_ids.price_total')
    def _compute_resource_task_total(self):
        for rec in self:
            rec.resource_task_total = sum(
                rec.mapped('resource_ids').filtered(
                    lambda r: r.resource_type == 'task').mapped(
                    'price_total'))

    @api.multi
    @api.depends('resource_ids', 'resource_ids.price_total')
    def _compute_resource_procurement_total(self):
        for rec in self:
            rec.resource_procurement_total = sum(
                rec.mapped('resource_ids').filtered(
                    lambda r: r.resource_type == 'procurement').mapped(
                    'price_total'))

    @api.multi
    @api.depends('resource_task_total', 'task_margin')
    def _compute_sale_task_total(self):
        for res in self:
            res.delivered_task = (
                    res.resource_task_total * (1 + res.task_margin/100)
            )

    @api.multi
    @api.depends('resource_procurement_total', 'procurement_margin')
    def _compute_sale_procurement_total(self):
        for res in self:
            margin = (1 + res.procurement_margin/100)
            res.delivered_material = (
                    res.resource_procurement_total * margin
            )

    @api.multi
    @api.depends('delivered_material', 'delivered_task')
    def _compute_target_revenue(self):
        for res in self:
            res.target_revenue = (
                res.delivered_material + res.delivered_task
            )

    @api.multi
    @api.depends('target_revenue', 'unit_amount')
    def _compute_wanted_price_unit(self):
        for res in self:
            res.wanted_price_unit = (
                res.target_revenue/res.unit_amount
            )

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
            if self.account_id.active_analytic_planning_version:
                self._compute_is_active

    @api.onchange('version_id')
    def on_change_version_id(self):
        self._compute_is_active

    @api.onchange('is_active')
    def on_change_is_active(self):
        self._compute_is_active

    @api.multi
    def copy(self, default=None):
        self.ensure_one()
        if default is None:
            default = {}
        default['parent_id'] = False
        default['analytic_line_plan_id'] = []
        res = super(BillingPlanLine, self).copy(default)
        return res

    @api.multi
    def unlink(self):
        billing = self.env['account.analytic.line.plan']
        res = super(BillingPlanLine, self).unlink()
        for billing in self:
            return res


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
