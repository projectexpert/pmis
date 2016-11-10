# -*- coding: utf-8 -*-
# © 2015 Eficent Business and IT Consulting Services S.L.
# (Jordi Ballester Alomar)
#
# © 2015 Serpent Consulting Services Pvt. Ltd.
# (Sudhir Arya)
#
# © 2016 Matmoz d.o.o.
# (Matjaž Mozetič)
#
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

import time
from openerp import api, fields, models
from openerp.tools.translate import _
from openerp.exceptions import Warning as UserError
from openerp.exceptions import ValidationError


class AnalyticResourcePlanLine(models.Model):

    _name = 'analytic.resource.plan.line'
    _description = "Analytic Resource Planning lines"
    _inherit = ['mail.thread', 'ir.needaction_mixin']

    @api.multi
    @api.depends('child_ids')
    def _has_child(self):
        res = {}
        for line in self:
            res[line.id] = False
            if line.child_ids:
                res[line.id] = True
        return res

    account_id = fields.Many2one(
        'account.analytic.account',
        'Analytic Account',
        required=True,
        ondelete='cascade',
        select=True,
        domain=[('type', '<>', 'view')],
        readonly=True,
        states={'draft': [('readonly', False)]}
    )
    name = fields.Char(
        'Activity description',
        required=True,
        readonly=True,
        states={'draft': [('readonly', False)]}
    )
    date = fields.Date(
        'Date',
        required=True,
        select=True,
        readonly=True,
        states={'draft': [('readonly', False)]},
        default=lambda *a: time.strftime('%Y-%m-%d')
    )
    state = fields.Selection(
        [
            ('draft', 'Draft'),
            ('confirm', 'Confirmed')
        ],
        'Status',
        select=True,
        required=True,
        readonly=True,
        help=' * The \'Draft\' status is '
             'used when a user is encoding a new and '
             'unconfirmed resource plan line. \n* '
             'The \'Confirmed\' status is used for to confirm '
             'the execution of the resource plan lines.',
        default='draft'
    )
    product_id = fields.Many2one(
        'product.product',
        'Product',
        readonly=True,
        required=True,
        states={'draft': [('readonly', False)]}
    )
    product_uom_id = fields.Many2one(
        'product.uom',
        'UoM',
        required=True,
        readonly=True,
        states={'draft': [('readonly', False)]}
    )
    unit_amount = fields.Float(
        'Planned Quantity',
        readonly=True,
        required=True,
        states={'draft': [('readonly', False)]},
        help='Specifies the quantity that has '
             'been planned.',
        default=1
    )
    notes = fields.Text(
        'Notes'
    )
    parent_id = fields.Many2one(
        'analytic.resource.plan.line',
        'Parent',
        readonly=True,
        ondelete='cascade'
    )
    child_ids = fields.One2many(
        comodel_name='analytic.resource.plan.line',
        inverse_name='parent_id',
        string='Child lines'
    )

    has_child = fields.Boolean(
        compute='_has_child',
        string="Child lines"
    )
    analytic_line_plan_ids = fields.One2many(
        'account.analytic.line.plan',
        'resource_plan_id',
        'Planned costs',
        readonly=True
    )
    price_unit = fields.Float(
        string='Cost Price',
        groups='project.group_project_manager',
    )
    price_total = fields.Float(
        store=False,
        compute='_compute_get_price_total',
        string='Total Cost',
        groups='project.group_project_manager',
    )
    resource_type = fields.Selection(
        selection=[('task', 'Task'), ('procurement', 'Procurement')],
        string='Type',
        required=True,
        default='task'
    )
    user_id = fields.Many2one(
        comodel_name='res.users',
        string='Assign To',
        ondelete='set null'
    )

    @api.multi
    def copy(self, default=None):
        self.ensure_one()
        if default is None:
            default = {}
        default['parent_id'] = False
        default['analytic_line_plan_ids'] = []
        res = super(AnalyticResourcePlanLine, self).copy(default)
        return res

    # TODO: Solve TypeError: can only concatenate list (not "NoneType") to list
    # on raise error
    @api.model
    def _prepare_analytic_lines(self):
        plan_version_obj = self.env['account.analytic.plan.version']
        journal_id = (
            self.product_id.expense_analytic_plan_journal_id
            and self.product_id.expense_analytic_plan_journal_id.id
            or False
        )
        general_account_id = (
            self.product_id.product_tmpl_id.property_account_expense.id
        )
        if not general_account_id:
            general_account_id = (
                self.product_id.categ_id.property_account_expense_categ.id
            )
        if not general_account_id:
            raise UserError(
                _(
                    'There is no expense account defined '
                    'for this product: "%s" (id:%d)'
                ) % (self.product_id.name, self.product_id.id,)
            )
        default_plan = plan_version_obj.search(
            [('default_resource_plan', '=', True)],
            limit=1
        )

        if not default_plan:
            raise UserError(
                _(
                    'No active planning version for resource '
                    'plan exists.'
                )
            )

        return [{
            'resource_plan_id': self.id,
            'account_id': self.account_id.id,
            'name': self.name,
            'date': self.date,
            'product_id': self.product_id.id,
            'product_uom_id': self.product_uom_id.id,
            'unit_amount': self.unit_amount,
            'amount': -1 * self.product_id.standard_price * self.unit_amount,
            'general_account_id': general_account_id,
            'journal_id': journal_id,
            'notes': self.notes,
            'version_id': default_plan.id,
            'currency_id': self.account_id.company_id.currency_id.id,
            # 'amount_currency': (
            #     -1 * self.product_id.standard_price * self.unit_amount
            # ),
        }]

    @api.model
    def create_analytic_lines(self):
        res = []
        line_plan_obj = self.env['account.analytic.line.plan']
        lines_vals = self._prepare_analytic_lines()
        for line_vals in lines_vals:
            line = line_plan_obj.create(line_vals)
        return res

    @api.model
    def _delete_analytic_lines(self):
        line_plan_obj = self.env['account.analytic.line.plan']
        ana_line = line_plan_obj.search([('resource_plan_id', '=', self.id)])
        ana_line.unlink()
        return True

    @api.multi
    def action_button_draft(self):
        for line in self:
            for child in line.child_ids:
                if child.state not in ('draft', 'plan'):
                    raise UserError(
                        _(
                            'All the child resource plan lines must '
                            ' be in Draft state.'
                        )
                    )
            line._delete_analytic_lines()
        return self.write({'state': 'draft'})

    @api.multi
    def action_button_confirm(self):
        for line in self:
            if line.unit_amount == 0:
                raise UserError(
                    _(
                        'Quantity should be greater than 0.'
                    )
                )
            if not line.child_ids:
                line.create_analytic_lines()
        return self.write({'state': 'confirm'})

    @api.onchange('product_id')
    def on_change_product_id(self):
        if self.product_id:
            self.name = self.product_id.name
            self.product_uom_id = (
                self.product_id.uom_id
                and self.product_id.uom_id.id
                or False
            )
            self.price_unit = self.product_id.standard_price

    @api.onchange('account_id')
    def on_change_account_id(self):
        if self.account_id:
            if self.account_id.date:
                self.date = self.account_id.date

    @api.multi
    def write(self, vals):
        analytic_obj = self.env['account.analytic.account']
        if 'account_id' in vals:
            analytic = analytic_obj.browse(vals['account_id'])
            if vals.get('date', False):
                vals['date'] = analytic.date
        return super(AnalyticResourcePlanLine, self).write(vals)

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
        return super(AnalyticResourcePlanLine, self).unlink()

    # PRICE DEFINITIONS
    @api.multi
    @api.depends('price_unit', 'unit_amount')
    def _compute_get_price_total(self):
        for resource in self:
            resource.price_total = resource.price_unit * resource.unit_amount

    @api.multi
    def _get_pricelist(self):
        self.ensure_one()
        partner_id = self._get_partner()
        if partner_id:
            if partner_id.property_product_pricelist:
                return partner_id.property_product_pricelist
        else:
            return False

    # RESOURCE TYPE
    @api.onchange('resource_type')
    def resource_type_change(self):
        if self.resource_type == 'procurement':
            self.user_id = False

    @api.multi
    @api.constrains('resource_type', 'product_uom_id')
    def _check_description(self):
        for resource in self:
            if self.resource_type == 'task' and (
                        self.product_uom_id.category_id != (
                            self.env.ref('product.uom_categ_wtime'))):
                raise ValidationError(_(
                    "When resource type is task, "
                    "the uom category should be time"))
