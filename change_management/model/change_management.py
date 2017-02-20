# -*- coding: utf-8 -*-
# Copyright (C) 2015 Matmoz d.o.o. (<http://www.matmoz.si>).
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openerp import tools, models, fields, api, _
import logging

_logger = logging.getLogger(__name__)


class CMChangeCategory (models.Model):
    _name = 'change.management.category'
    _description = 'Change log category table'

    name = fields.Char(string='Change Category', required=True, translate=True)


class CMProximity (models.Model):
    _name = 'change.management.proximity'
    _description = 'Change log proximity table'

    name = fields.Char(string='Proximity', required=True, translate=True)


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

    # ##### FIELDS #####  #

    name = fields.Char(
        'Request Id',
        default="/",
        readonly=True,
        states={'draft': [('readonly', False)]},
        help='''
Change label. Can be changed as long as change is in state 'draft'.
        '''
    )

    description = fields.Char(
        string='Request Description',
        help='''
Short description of the change.

Project changes are characteristics, circumstances or
features of the project environment that may have an
adverse effect on the project in the form of budget,
schedule, deliverables and results.

Stakeholder requirements can be considered and
managed as changes, since we're changing the project
charter and scope definition.

The user requirements of the project must be defined and
documented. Approval and confirmation must be obtained
before the project can proceed. To obtain agreement about
needs:

* Separate needs from wants
* Group the needs that are similar
* Prioritise needs (eg essential, nice to have)
* Identify any conflicting needs
* Negotiate agreement between stakeholders with
   conflicting needs

This process often requires a number of meetings with
stakeholders. Stakeholders often express their needs in
terms of a particular product or solution to the problem,
which has created the need for the project in the first
place. It is important to re-state the agreed needs in
terms of “what the end product/service(s) of the project
should do”.
Stating the agreed needs in functional terms permits the
project manager to offer a range of solutions to the client
or key stakeholders. If the project outcomes are restricted
to solutions offered by key stakeholders too early in the
analysis process important alternative options might be
overlooked. Document the final set of agreed requirements
and obtain sign-off from all key stakeholders.
        '''
    )
    project_id = fields.Many2one(
        comodel_name='project.project',
        string='Project',
        ondelete='set null',
        readonly=True,
        states={'draft': [('readonly', False)]},
        required=True,
    )
    author_id = fields.Many2one(
        'res.users', 'Requestor', required=True,
        default=lambda self: self.env.user.id
    )
    stakeholder_id = fields.Many2one(
        'res.partner', string='Proposer'
    )
    color = fields.Integer(
        'Color'
    )

    date_confirmed = fields.Date(
        string='Confirmation Date',
        readonly=True,
        help="Date of the change confirmation. Auto populated."
    )
    confirmed_id = fields.Many2one(
        'res.users',
        string='Confirmed by',
        readonly=True
    )
    date_approved = fields.Datetime(
        string='Approval Date',
        readonly=True
    )
    approved_id = fields.Many2one(
        'res.users',
        string='Approved by',
        readonly=True
    )
    date_modified = fields.Date(
        'Date Revised', help="Date of last revision."
    )
    change_category_id = fields.Many2one(
        'change.management.category', 'Change Category',
        default=lambda s: s._get_default_category(),
        help='''
Change Category: The type of change in terms of the project's or business'
chosen categories (e.g. Schedule, quality, legal etc.)
        '''
    )
    description_cause = fields.Html(
        'Change'
    )
    description_event = fields.Html(
        'Reason'
    )
    description_effect = fields.Html(
        'Effect'
    )
    proximity_id = fields.Many2one(
        'change.management.proximity', 'Proximity',
        help='''
Proximity: This would typically state how close to the present time the change
event is anticipated to happen (e.g. for project changes Imminent, within
stage, within project, beyond project). Proximity should be recorded in
accordance with the project's chosen scales or business continuity time scales.
        '''
    )
    change_response_ids = fields.One2many(
        'project.task', 'change_id', 'Response Ids'
    )
    change_response_count = fields.Integer(
        compute='_change_response_count', type='integer'
    )
    state = fields.Selection(
        selection="_get_states",
        default='draft',
        readonly=True,
        string='State',
        states={'draft': [('readonly', False)]},
        # track_visibility='on_change'
    )
    change_owner_id = fields.Many2one(
        'res.users', 'Change Manager',
        help='''
Change Manager: The person responsible for managing the change (there can be
only one change owner per change), change ownership is assigned to a managerial
level, in case of business continuity to a C-level manager.
        '''
    )

    company_id = fields.Many2one(
        'res.company', string='Company',
        required=True, readonly=True, states={'draft': [('readonly', False)]},
        default=lambda self: self.env.user.company_id.id,
    )

    # ##### DEFINITIONS #####  #

    @api.model
    def _get_states(self):
        states = [
            ('draft', 'Draft'),
            ('active', 'Confirmed'),
            ('accepted', 'Approved'),
            ('in_progress', 'In progress'),
            ('done', 'Done'),
            ('rejected', 'Rejected'),
            ('withdraw', 'Withdrawn'),
            ('deferred', 'Deferred')
        ]
        return states

    @api.depends('change_response_ids')
    def _change_response_count(self):
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

    @api.multi
    def set_in_progress(self):
        self.write({'state': 'in_progress'})

    @api.multi
    def set_state_done(self):
        self.write({'state': 'done'})

    @api.multi
    def set_state_rejected(self):
        self.write({'state': 'rejected'})

    @api.multi
    def set_state_deferred(self):
        self.write({'state': 'deferred'})

    @api.multi
    def set_state_withdrawn(self):
        self.write({'state': 'withdraw'})

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
    def write(self, vals):
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
    def message_get_suggested_recipients(self):
        recipients = super(
            CMChange, self
        ).message_get_suggested_recipients()
        try:
            for change in self:
                if change.stakeholder_id:
                    change._message_add_suggested_recipient(
                        recipients, partner=change.stakeholder_id,
                        reason=_('Customer')
                    )
                elif change.email_from:
                    change._message_add_suggested_recipient(
                        recipients, email=change.email_from,
                        reason=_('Customer Email')
                    )
        except AccessError:
            # no read access rights -> just ignore suggested recipients
            # because this imply modifying followers
            pass
        return recipients

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

    @api.multi
    def message_update(self, msg, update_vals=None):
        """ Override to update the change according to the email. """
        email_list = self.email_split(msg)
        stakeholder_ids = filter(
            None, self._find_partner_from_emails(email_list)
        )
        self.message_subscribe(stakeholder_ids)
        return super(CMChange, self).message_update(
            msg, update_vals=update_vals
        )

    # Some v10 related entries

    # @api.multi
    # @api.returns('mail.message', lambda value: value.id)
    # def message_post(self, subtype=None, **kwargs):
    #     """ Overrides mail_thread message_post so that we can set
    #      the date of last action field when a new message is posted on
    #      the change.
    #     """
    #     self.ensure_one()
    #     mail_message = super(CMChange, self).message_post(
    #         subtype=subtype, **kwargs
    #     )
    #     if subtype:
    #         self.sudo().write({'date_modified': fields.Datetime.now()})
    #     return mail_message

    # @api.multi
    # def message_get_email_values(self, notif_mail=None):
    #     self.ensure_one()
    #     res = super(CMChange, self).message_get_email_values(
    #         notif_mail=notif_mail)
    #     headers = {}
    #     if res.get('headers'):
    #         try:
    #             headers.update(safe_eval(res['headers']))
    #         except Exception:
    #             pass
    #     if self.project_id:
    #         current_objects = filter(
    #             None, headers.get('X-Odoo-Objects', '').split(',')
    #         )
    #         current_objects.insert(
    #             0, 'project.project-%s, ' % self.project_id.id
    #         )
    #         headers['X-Odoo-Objects'] = ','.join(current_objects)
    #     if self.tag_ids:
    #         headers['X-Odoo-Tags'] = ','.join(self.tag_ids.mapped('name'))
    #     res['headers'] = repr(headers)
    #     return res


class Project(models.Model):
    _inherit = "project.project"

    # @api.v7
    # def _get_alias_models(self, cr, uid, context=None):
    #     res = super(Project, self)._get_alias_models(cr, uid, context=context)
    #     res.append(("change.management.change", "Change Requests"))
    #     return res

    @api.model
    def _get_alias_models(self):
        res = super(Project, self)._get_alias_models()
        res.append(("change.management.change", "Change Requests"))
        return res
