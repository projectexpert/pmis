# -*- coding: utf-8 -*-
# Copyright (C) 2017 Matmoz d.o.o. (<http://www.matmoz.si>).
# Copyright (C) 2018 Luxim d.o.o. (<http://www.matmoz.si>).
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openerp import tools, models, fields, api, _
import logging

_logger = logging.getLogger(__name__)

# Change Category
class CMChangeCategory (models.Model):
    _name = 'change.management.category'
    _description = 'Change log category table'

    name = fields.Char(
        string='Category',
        required=True,
        translate=True
    )


# Change Proximity
class CMProximity (models.Model):
    _name = 'change.management.proximity'
    _description = 'Change log proximity table'

    name = fields.Char(
        string='Proximity',
        required=True,
        translate=True
    )


# Change Request
class CMChange (models.Model):
    _name = 'change.management.change'
    _description = 'Change'
    _inherit = ['mail.thread', 'ir.needaction_mixin']
    _order = 'id desc'

    # ##### Track state changes #####  #
    _track = {
        'state': {
            'change_management.mt_change_draft': (
                lambda self, cr, uid, obj,
                ctx=None: obj['state'] in ['draft']
            ),
            'change_management.mt_change_active': (
                lambda self, cr, uid, obj,
                ctx=None: obj['state'] in ['active']
            ),
            'change_management.mt_change_accepted': (
                lambda self, cr, uid, obj,
                ctx=None: obj['state'] in ['accepted']
            ),
            'change_management.mt_change_in_progress': (
                lambda self, cr, uid, obj,
                ctx=None: obj['state'] in ['in_progress']
            ),
            'change_management.mt_change_done': (
                lambda self, cr, uid, obj,
                ctx=None: obj['state'] in ['done']
            ),
            'change_management.mt_change_rejected': (
                lambda self, cr, uid, obj,
                ctx=None: obj['state'] in ['rejected']
            ),
            'change_management.mt_change_withdrawn': (
                lambda self, cr, uid, obj,
                ctx=None: obj['state'] in ['withdrawn']
            ),
            'change_management.mt_change_deferred': (
                lambda self, cr, uid, obj,
                ctx=None: obj['state'] in ['deferred']
            )
        }
    }

    # ##### define CR code #####  #

    @api.model
    def create(self, vals):
        if vals.get('name', '/'):
            vals['name'] = self.env['ir.sequence'].get(
                'change.management.change')
        return super(CMChange, self).create(vals)

    @api.multi
    def copy(self, default=None):
        self.ensure_one()
        if default is None:
            default = {}
        default['name'] = self.env['ir.sequence'].get(
            'change.management.change')
        return super(CMChange, self).copy(default)

    # Risk management values
    @api.depends('impact_inherent', 'probability_inherent')
    def _calculate_expected_inherent_value(self):
        for record in self:
            record.expected_value_inherent = (
                    record.impact_inherent * record.probability_inherent
            )

    @api.depends('impact_residual', 'probability_residual')
    def _calculate_expected_residual_value(self):
        for record in self:
            record.expected_value_residual = (
                    record.impact_residual * record.probability_residual
            )

    # ##### FIELDS #####  #

    name = fields.Char(
        'Request Id',
        default="/",
        readonly=True,
        # states={'draft': [('readonly', False)]},
    )

    description = fields.Char(
        string='Description',
        readonly=True,
        required=True,
        states={'draft': [('readonly', False)],
                'active': [('readonly', False)]},
        help='Short description of the request.'
    )
    project_id = fields.Many2one(
        comodel_name='project.project',
        string='Project',
        ondelete='set null',
        readonly=True,
        states={'draft': [('readonly', False)]},
        required=True,
        help="The project where the change request was initiated."
    )
    author_id = fields.Many2one(
        'res.users', 'Requestor', required=True,
        default=lambda self: self.env.user,
        readonly=True,
        states={'draft': [('readonly', False)]},
        help="The author of the initial request."
    )
    stakeholder_id = fields.Many2one(
        'res.partner', string='Proposer',
        readonly=True,
        states={'draft': [('readonly', False)],
                'active': [('readonly', False)]},
        help="The stakeholder that proposes the  processing of the request."
    )
    color = fields.Integer(
        'Color', default=0
    )

    date_confirmed = fields.Date(
        string='Confirmation Date',
        readonly=True,
        help="Date of the change confirmation. Auto populated."
    )
    confirmed_id = fields.Many2one(
        'res.users',
        string='Confirmed by',
        readonly=True,
        help="The person that confirmed the change. Auto populated."
    )
    date_approved = fields.Datetime(
        string='Approval Date',
        readonly=True
    )
    approved_id = fields.Many2one(
        'res.users',
        string='Approved by',
        readonly=True,
        help="The person that approved the change. Auto populated."
    )
    date_modified = fields.Date(
        'Date Revised', help="Date of last revision."
    )
    change_category_id = fields.Many2one(
        'change.management.category', 'Category',
        default=lambda s: s._get_default_category(),
        readonly=True,
        states={'draft': [('readonly', False)],
                'active': [('readonly', False)]},
        help="Change Category: "
        "The type of change in terms of the project's or business"
        "chosen categories (e.g. Schedule, quality, legal etc.)"
    )
    description_event = fields.Html(
        'Reason',
        readonly=True,
        states={
            'draft': [('readonly', False)],
            'active': [('readonly', False)]
        },
    )
    proximity_id = fields.Many2one(
        'change.management.proximity', 'Proximity',
        help="Proximity: "
        "This would typically state how close to the present time the change "
        "event is anticipated to happen (e.g. for project changes Imminent, "
        "within stage, within project, beyond project). Proximity should be "
        "recorded in accordance with the project's chosen scales or business "
        "continuity time scales."
    )
    change_response_ids = fields.One2many(
        comodel_name='project.task',
        inverse_name='change_id',
        string='Responses'
    )
    change_response_count = fields.Integer(
        compute='_compute_response_count', type='integer'
    )
    state = fields.Selection(
        selection="_get_states",
        default='draft',
        readonly=True,
        string='State',
        states={'draft': [('readonly', False)]},
    )
    type_id = fields.Selection(
        selection="_get_type",
        default='change',
        readonly=True,
        string="Request Type",
        states={'draft': [('readonly', False)]},
        help="Type: "
             "Is this an original requirement, a change in an undergoing "
             "project or a risk?"
    )
    change_owner_id = fields.Many2one(
        'res.users',
        string='Responsible',
        readonly=True,
        states={'draft': [('readonly', False)],
                'active': [('readonly', False)]},
        help="Change Manager: "
        "The person responsible for managing the change (there can be "
        "only one change owner per change), change ownership is assigned "
        "to a managerial level, in case of business continuity to a "
        "C-level manager."
    )

    company_id = fields.Many2one(
        'res.company', string='Company',
        required=True, readonly=True, states={'draft': [('readonly', False)]},
        default=lambda self: self.env.user.company_id,
    )

    kanban_state = fields.Selection(
        [
            ('normal', 'In Progress'),
            ('on_hold', 'On Hold'),
            ('done', 'Ready for next stage')
        ],
        'Kanban State',
        track_visibility='onchange',
        required=False,
        copy=False,
        default='normal'
    )
    # risk management related
    impact_inherent = fields.Integer(
        'Inherent Impact', required=True,
        default=0,
        help="Inherent Impact: "
        "The result of a particular threat or opportunity actually "
        "occurring, or the anticipation of such a result. This is the "
        "pre-response value, common used scales are 1 to 10 or 1 to 100."
    )
    impact_residual = fields.Integer(
        'Residual Impact', required=True,
        default=0,
        help="Residual Impact: "
        "The result of a particular threat or opportunity actually "
        "occurring, or the anticipation of such a result. This is the "
        "post-response value, common used scales are 1 to 10 or 1 to 100."
    )
    probability_inherent = fields.Integer(
        'Inherent Probability', required=True,
        default=0,
        help="Inherent Probability: The evaluated likelihood of a particular "
        "threat or opportunity actually happening, including a consideration "
        "of the frequency with which this may arise. This is the pre-response"
        " value, common used scales are 1 to 10 or 1 to 100."
    )
    probability_residual = fields.Integer(
        'Residual Probability', required=True,
        default=0,
        help="Residual Probability: "
        "The evaluated likelihood of a particular threat or opportunity "
        "actually happening, including a consideration of the frequency "
        "with which this may arise. This is the post-response value, "
        "common used scales are 1 to 10 or 1 to 100."
    )
    expected_value_inherent = fields.Float(
        compute='_calculate_expected_inherent_value', method=True,
        string='Expected Inherent Value', store=True,
        help="Expected Value. "
        "Cost of inherent impact * inherent probability. This is the "
        "pre-response value."
    )
    expected_value_residual = fields.Float(
        compute='_calculate_expected_residual_value', method=True,
        string='Expected Residual Value', store=True,
        help="Expected Value. "
        "Cost of residual impact * residual probability. This is the "
        "post-response value."
    )

    account_id = fields.Many2one(
        related='project_id.analytic_account_id'
    )
    deliverable_ids = fields.One2many(
        comodel_name="analytic.billing.plan.line",
        inverse_name="change_id",
        string="Deliverable Lines",
        readonly=False,
        copy=True,
        states={'draft': [('readonly', False)],
                'active': [('readonly', False)]},
    )

    # ##### DEFINITIONS #####  #

    @api.multi
    def name_get(self):
        """
        Display [Reference] Description if reference is defined
        otherwise display [Name] Description
        """
        result = []
        for cr in self:
            if cr.description:
                formatted_name = u'[{}] {}'.format(cr.name, cr.description)
            else:
                formatted_name = u'[{}]'.format(cr.name)
            result.append((cr.id, formatted_name))
        return result

    @api.model
    def _get_states(self):
        states = [
            ('draft', 'Draft'),
            ('active', 'Confirmed'),
            ('accepted', 'Accepted'),
            ('in_progress', 'In progress'),
            ('done', 'Done'),
            ('rejected', 'Rejected'),
            ('withdraw', 'Withdrawn'),
            ('deferred', 'Deferred')
        ]
        return states

    @api.model
    def _get_type(self):
        types = [
            ('change', 'Change'),
            ('requirement', 'Requirement'),
            ('risk', 'Risk')
        ]
        return types

    @api.depends('change_response_ids')
    def _compute_response_count(self):
        for record in self:
            record.change_response_count = len(record.change_response_ids)

    @api.multi
    def set_state_draft(self):
        self.write({'state': 'draft'})
        self.confirmed_id = self.approved_id = []
        self.date_confirmed = self.approval_date = ''

    @api.multi
    def set_state_active(self):
        self.write({'state': 'active'})
        self.confirmed_id = self.env.user
        self.date_confirmed = fields.Datetime.now()

    @api.multi
    def set_state_accepted(self):
        self.write({'state': 'accepted'})
        self.approved_id = self.env.user
        self.date_approved = fields.Datetime.now()
        self.date_modified = fields.Datetime.now()

    @api.multi
    def set_in_progress(self):
        self.write({'state': 'in_progress'})
        self.date_modified = fields.Datetime.now()

    @api.multi
    def set_state_done(self):
        self.write({'state': 'done'})
        self.date_modified = fields.Datetime.now()

    @api.multi
    def set_state_rejected(self):
        self.write({'state': 'rejected'})
        self.date_modified = fields.Datetime.now()

    @api.multi
    def set_state_deferred(self):
        self.write({'state': 'deferred'})
        self.date_modified = fields.Datetime.now()

    @api.multi
    def set_state_withdrawn(self):
        self.write({'state': 'withdraw'})
        self.date_modified = fields.Datetime.now()

    @api.multi
    def _subscribe_extra_followers(self, vals):
        user_ids = [
            vals[x] for
            x in
            ['author_id', 'change_owner_id'] if
            x in
            vals if not
            vals[x] is False
        ]
        if len(user_ids) > 0:
            self.message_subscribe_users(
                user_ids=user_ids
            )

        changes = self.read(
            ['message_follower_ids', 'change_response_ids']
        )
        for change in changes:
            if 'change_response_ids' in change and change[
                'change_response_ids'
            ]:
                task_ob = self.env['project.task']
                task_ob.message_subscribe(
                    change['change_response_ids'], change[
                        'message_follower_ids'
                    ]
                )

    @api.multi
    def write_user_followers(self, vals):
        ret = super(CMChange, self).write(
            vals
        )
        self._subscribe_extra_followers(vals)
        return ret

    @api.model
    def _get_default_category(self):
        return self.env.ref(
            'change_management.change_management_new',
            False) and self.env.ref(
            'change_management.change_management_new') or self.env[
                   'change.management.category']

    @api.multi
    def open_deliverable_line(self):
        for self in self:
            domain = [
                ('change_id', '=', self.id)
            ]
            cr_id = 0
            ac_id = 9
            if self.state in ('draft', 'active'):
                cr_id = self.id
                ac_id = self.account_id.id
            return {
                'name': _('Deliverable Lines'),
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'tree,form,graph',
                'res_model': 'analytic.billing.plan.line',
                'target': 'current',
                'domain': domain,
                'context': {
                    'tree_view_ref': 'analytic_billing_plan.' +
                                     'view_analytic_billing_plan_line_tree',
                    'form_view_ref': 'analytic_billing_plan.' +
                                     'view_analytic_billing_plan_line_form',
                    'default_change_id': cr_id,
                    'default_account_id': ac_id
                }
            }

    # ##### create CR from mail #####  #

    @api.model
    def message_get_reply_to(self, res_ids, default=None):
        """ Override to get the reply_to of the parent project. """
        changes = self.browse(res_ids)
        project_ids = set(changes.mapped('project_id').ids)
        aliases = self.env['project.project'].message_get_reply_to(
            list(project_ids), default=default
        )
        return dict(
            (
                change.id, aliases.get(
                    change.project_id and change.project_id.id or 0, False
                )
            ) for change in changes
        )

    @api.multi
    def email_split(self, msg):
        email_list = tools.email_split(
            (msg.get('to') or '') + ',' + (msg.get('cc') or ''))
        # check left-part is not already an alias
        return filter(lambda x: x.split('@')[0] not in self.mapped(
            'project_id.alias_name'), email_list)

    @api.model
    def message_new(self, msg, custom_values=None):
        """ Overrides mail_thread message_new that is called by the mailgateway
            through message_process.
            This override updates the document according to the email.
        """
        # remove default author when going through the mail gateway. Indeed we
        # do not want to explicitly set user_id to False; however we do not
        # want the gateway user to be responsible if no other responsible is
        # found.
        create_context = dict(self.env.context or {})
        create_context['default_user_id'] = False
        defaults = {
            'description': msg.get('subject') or _("No Subject"),
            'email_from': msg.get('from'),
            'email_cc': msg.get('cc'),
            'stakeholder_id': msg.get('author_id', False)
        }
        if custom_values:
            defaults.update(custom_values)

        res_id = super(
            CMChange,
            self.with_context(create_context)
        ).message_new(msg, custom_values=defaults)
        change = self.browse(res_id)
        email_list = change.email_split(msg)
        stakeholder_ids = filter(
            None, change._find_partner_from_emails(email_list)
        )
        change.message_subscribe(stakeholder_ids)
        return res_id


class Project(models.Model):
    _inherit = "project.project"

    @api.model
    def _get_alias_models(self):
        res = super(Project, self)._get_alias_models()
        res.append(("change.management.change", "Change Requests"))
        return res

    change_ids = fields.One2many(
        comodel_name='change.management.change',
        inverse_name='project_id',
        string='Changes',
        domain=[('type_id', '=', 'change')]
    )

    requirement_ids = fields.One2many(
        comodel_name='change.management.change',
        inverse_name='project_id',
        string='Requirements',
        domain=[('type_id', '=', 'requirement')]
    )

    risk_ids = fields.One2many(
        comodel_name='change.management.change',
        inverse_name='project_id',
        string='Changes',
        domain=[('type_id', '=', 'risk')]
    )

    cr_count = fields.Integer(
        compute='_compute_cr_count', type='integer'
    )

    req_count = fields.Integer(
        compute='_compute_req_count', type='integer'
    )

    risk_count = fields.Integer(
        compute='_compute_risk_count', type='integer'
    )

    @api.depends('change_ids')
    def _compute_cr_count(self):
        for record in self:
            record.cr_count = len(record.change_ids)

    @api.depends('requirement_ids')
    def _compute_req_count(self):
        for record in self:
            record.req_count = len(record.requirement_ids)

    @api.depends('risk_ids')
    def _compute_risk_count(self):
        for record in self:
            record.risk_count = len(record.risk_ids)
