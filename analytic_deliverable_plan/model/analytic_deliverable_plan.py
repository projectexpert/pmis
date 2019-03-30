# -*- coding: utf-8 -*-
#    Copyright 2016 MATMOZ, Slovenia (Matjaž Mozetič)
#    Copyright 2018 EFICENT (Jordi Ballester Alomar)
#    Copyright 2018 LUXIM, Slovenia (Matjaž Mozetič)
#    Together as the Project Expert Team
#    License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

import time
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class AnalyticDeliverablePlanLine(models.Model):

    _name = 'analytic.deliverable.plan.line'
    _description = "Analytic Deliverable Planning lines"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    account_id = fields.Many2one(
        comodel_name='account.analytic.account',
        string='Analytic Account',
        required=True,
        ondelete='cascade',
        index=True,
        readonly=True,
        states={'draft': [('readonly', False)]}
    )
    name = fields.Char(
        string='Activity description',
        required=True,
        readonly=True,
        states={'draft': [('readonly', False)]}
    )
    date = fields.Date(
        string='Date',
        required=True,
        index=True,
        readonly=True,
        states={'draft': [('readonly', False)]},
        default=lambda *a: time.strftime('%Y-%m-%d')
    )
    state = fields.Selection(
        selection=[
            ('draft', 'Draft'),
            ('confirm', 'Confirmed')
        ],
        string='Status',
        index=True,
        required=True,
        readonly=True,
        help=' * The \'Draft\' status is '
             'used when a user is encoding a new and '
             'unconfirmed deliverable plan line. \n* '
             'The \'Confirmed\' status is used for to confirm '
             'the execution of the deliverable plan lines.',
        default='draft'
    )
    product_id = fields.Many2one(
        comodel_name='product.product',
        string='Product',
        readonly=True,
        required=True,
        states={'draft': [('readonly', False)]}
    )
    product_uom_id = fields.Many2one(
        comodel_name='product.uom',
        string='UoM',
        required=True,
        readonly=True,
        states={'draft': [('readonly', False)]}
    )
    unit_amount = fields.Float(
        string='Planned unit_amount',
        readonly=True,
        required=True,
        states={'draft': [('readonly', False)]},
        help='Specifies the quantity that has '
             'been planned.',
        default=1
    )
    analytic_line_plan_ids = fields.One2many(
        comodel_name='account.analytic.line.plan',
        inverse_name='deliverable_plan_id',
        string='Planned revenue',
        readonly=True
    )
    price_unit = fields.Float(
        string='Sale Price',
        groups='project.group_project_manager',
    )
    price_total = fields.Float(
        store=False,
        compute='_compute_get_price_total',
        string='Total Revenue',
        groups='project.group_project_manager',
    )
    company_id = fields.Many2one(
        related='account_id.company_id',
        string='Company',
        store=True,
        readonly=True
    )
    currency_id = fields.Many2one(
        related="company_id.currency_id",
        string="Currency",
        readonly=True
    )

    # resources references
    resource_ids = fields.One2many(
        comodel_name='analytic.resource.plan.line',
        inverse_name='deliverable_id',
        string='Resource Lines',
        copy=True,
    )

    # price analysis hints
    task_margin = fields.Float(
        string='Work Margin (%)',
        help='Sale Margin for work in %',
        groups='project.group_project_manager',
        default='66',
        required=True
    )
    procurement_margin = fields.Float(
        string='Material Margin (%)',
        help='Sale Margin for materials in %',
        groups='project.group_project_manager',
        default='66',
        required=True
    )
    target_revenue = fields.Float(
        string='Prop. total price',
        help='Target budget computed from costs and wanted margin.',
        groups='project.group_project_manager',
        compute='_compute_target_revenue'
    )
    resource_task_total = fields.Float(
        compute='_compute_resource_task_total',
        string='Work cost',
        store=True
    )
    resource_procurement_total = fields.Float(
        compute='_compute_resource_procurement_total',
        string='Material cost',
        store=True
    )
    delivered_task = fields.Float(
        compute='_compute_sale_task_total',
        string='Work sale price',
        help='Total tasks sale price',
        store=True
    )
    delivered_material = fields.Float(
        compute='_compute_sale_procurement_total',
        string='Material sale price',
        help='Total materials sale price',
        store=True
    )
    wanted_price_unit = fields.Float(
        compute='_compute_wanted_price_unit',
        string='Prop. price/unit',
        help='Proposed sale price per UoM'
    )
    projection = fields.Float(
        compute='_compute_projection',
        string='Projected profit/loss',
        help='Projected profit/loss'
             'Calculated as: Total revenue - Total costs'
    )

    @api.multi
    def copy(self, default=None):
        self.ensure_one()
        if default is None:
            default = {}
        default['analytic_line_plan_ids'] = []
        res = super(AnalyticDeliverablePlanLine, self).copy(default)
        return res

    @api.model
    def _prepare_analytic_lines(self):
        journal_id = (
            self.product_id.revenue_analytic_plan_journal_id
            and self.product_id.revenue_analytic_plan_journal_id.id
            or False
        )
        general_account_id = (
            self.product_id.product_tmpl_id.property_account_income_id.id
        )
        if not journal_id:
            raise ValidationError(
                _('There is no analytic plan journal for product %s')
                % self.product_id.name
            )
        if not general_account_id:
            general_account_id = (
                self.product_id.categ_id.property_account_income_categ_id.id
            )
        if not general_account_id:
            raise ValidationError(
                _('There is no revenue account defined '
                  'for this product: "%s" (id:%d)')
                % (self.product_id.name, self.product_id.id,)
            )

        return [{
            'deliverable_plan_id': self.id,
            'account_id': self.account_id.id,
            'name': self.name,
            'date': self.date,
            'product_id': self.product_id.id,
            'product_uom_id': self.product_uom_id.id,
            'unit_amount': self.unit_amount,
            'unit_price': self.price_unit,
            'amount': -1 * self.price_total,
            'general_account_id': general_account_id,
            'journal_id': journal_id,
            'currency_id': self.account_id.company_id.currency_id.id,
        }]

    @api.model
    def create_analytic_lines(self):
        line_plan_obj = self.env['account.analytic.line.plan']
        lines_vals = self._prepare_analytic_lines()
        for line_vals in lines_vals:
            line_plan_obj.create(line_vals)

    @api.model
    def _delete_analytic_lines(self):
        line_plan_obj = self.env['account.analytic.line.plan']
        ana_line = line_plan_obj.search(
            [('deliverable_plan_id', '=', self.id)])
        ana_line.unlink()
        return True

    @api.multi
    def action_button_draft(self):
        for line in self:
            line._delete_analytic_lines()
        return self.write({'state': 'draft'})

    @api.multi
    def action_button_confirm(self):
        for line in self:
            line.create_analytic_lines()
        return self.write({'state': 'confirm'})

    @api.onchange('product_id')
    def on_change_product_id(self):
        if self.product_id:
            self.name = self.product_id.name
            self.product_uom_id = (
                    self.product_id.uom_id and
                    self.product_id.uom_id.id or
                    False
            )
            self.price_unit = self.product_id.lst_price

    @api.multi
    def write(self, vals):
        analytic_obj = self.env['account.analytic.account']
        if 'account_id' in vals:
            analytic = analytic_obj.browse(vals['account_id'])
            if vals.get('date', False):
                vals['date'] = analytic.date
        return super(AnalyticDeliverablePlanLine, self).write(vals)

    @api.multi
    def unlink(self):
        for line in self:
            if line.analytic_line_plan_ids:
                raise ValidationError(
                    _('You cannot delete a record that refers to '
                      'analytic plan lines')
                )
        return super(AnalyticDeliverablePlanLine, self).unlink()

    # PRICE DEFINITIONS
    @api.multi
    @api.depends('price_unit', 'unit_amount')
    def _compute_get_price_total(self):
        for deliverable in self:
            deliverable.price_total = (
                    deliverable.price_unit * deliverable.unit_amount)

    @api.multi
    def _get_pricelist(self):
        self.ensure_one()
        partner_id = self._get_partner()
        if partner_id:
            if partner_id.property_product_pricelist:
                return partner_id.property_product_pricelist
        else:
            return False

    @api.multi
    def action_open_view_rpl_form(self):
        self.with_context(view_buttons=True)
        view = {
            'name': _('Details'),
            'view_type': 'form',
            'view_mode': 'form,tree',
            'res_model': 'analytic.deliverable.plan.line',
            'view_id': False,
            'type': 'ir.actions.act_window',
            'target': 'current',
            'res_id': self.id,
            'context': self.env.context
        }
        return view

    # resources
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
                    res.resource_task_total * (1 + res.task_margin / 100)
            )

    # procurements
    @api.multi
    @api.depends('resource_procurement_total', 'procurement_margin')
    def _compute_sale_procurement_total(self):
        for res in self:
            margin = (1 + res.procurement_margin / 100)
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
            if res.unit_amount != 0:
                res.wanted_price_unit = (
                        res.target_revenue / res.unit_amount
                )
            else:
                res.wanted_price_unit = 0

    @api.multi
    @api.depends(
        'price_total', 'resource_procurement_total', 'resource_task_total'
    )
    def _compute_projection(self):
        for res in self:
            res.projection = (
                    res.price_total
                    - res.resource_procurement_total
                    - res.resource_task_total
            )


class ResourcePlanLine(models.Model):

    _inherit = 'analytic.resource.plan.line'

    deliverable_id = fields.Many2one(
        comodel_name='analytic.deliverable.plan.line',
        string='Deliverable',
        ondelete='cascade'
    )

    @api.onchange('deliverable_id')
    def on_change_deliverable_id(self):
        if self.deliverable_id:
            self.account_id = self.deliverable_id.account_id
