# -*- coding: utf-8 -*-
##############################################################################
#
#    Odoo, Open Source Enterprise Management Solution
#
#    Copyright (C) 2015 Matmoz d.o.o. (<http://www.matmoz.si>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
from openerp import models, fields, api
from datetime import date
import logging

_logger = logging.getLogger(__name__)

_CHANGE_STATE = [
    ('draft', 'Draft'),
    ('active', 'Active'),
    ('rejected', 'Rejected'),
    ('accepted', 'Accepted'),
    ('deferred', 'Deferred')
]


class change_management_change_category (models.Model):
    _name = 'change.management.category'
    _description = 'Change log category table'

    name = fields.Char(string='Change Category', size=64, required=True)

change_management_change_category()


class change_management_proximity (models.Model):
    _name = 'change.management.proximity'
    _description = 'Change log proximity table'

    name = fields.Char(string='Proximity', size=64, required=True)

change_management_proximity()


class change_management_change (models.Model):
    _name = 'change.management.change'
    _description = 'Change'
    _inherit = ['mail.thread', 'ir.needaction_mixin']

    _track = {
        'state': {
            'change.mt_change_draft': lambda self, cr, uid, obj, ctx=None: obj['state'] in ['draft'],
            'change.mt_change_active': lambda self, cr, uid, obj, ctx=None: obj['state'] in ['active'],
            'change.mt_change_rejected': lambda self, cr, uid, obj, ctx=None: obj['state'] in ['rejected'],
            'change.mt_change_accepted': lambda self, cr, uid, obj, ctx=None: obj['state'] in ['accepted'],
            'change.mt_change_deferred': lambda self, cr, uid, obj, ctx=None: obj['state'] in ['deferred']
        }
    }

    @api.depends('change_response_ids')
    def _change_response_count(self):
            for record in self:
                record.change_response_count = len(record.change_response_ids)

    @api.one
    def set_state_draft(self):
        return self.write({'state': 'draft'})

    @api.one
    def set_state_active(self):
        return self.write({'state': 'active'})

    @api.one
    def set_state_rejected(self):
        return self.write({'state': 'rejected'})

    @api.one
    def set_state_accepted(self):
        return self.write({'state': 'accepted'})

    @api.one
    def set_state_deferred(self):
        return self.write({'state': 'deferred'})

    #
    # FIELDS
    #

    name = fields.Char(
        'Request Id', size=64, required=True, readonly=True, states={'draft': [('readonly', False)]}, select=True,
        help='''
Change label. Can be changed as long as change is in state 'draft'.
        '''
    )
    description = fields.Char(
        string='Request Description', size=64, help='''
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
        'project.project', 'Project', required=True
    )
    author_id = fields.Many2one(
        'res.users', 'Requestor', required=True
    )
    stakeholder_id = fields.Many2one(
        'project.hr.stakeholder', string='Proposer'
    )
    color = fields.Integer(
        'Color'
    )
    date_registered = fields.Date(
        'Date Registered', required=True, help="Date of the change registered. Auto populated."
    )
    date_modified = fields.Date(
        'Date Revised', help="Date of last revision."
    )
    change_category_id = fields.Many2one(
        'change.management.category', 'Change Category', required=True,
        help='''
Change Category: The type of change in terms of the project's or business' chosen categories
(e.g. Schedule, quality, legal etc.)
        '''
    )
    description_cause = fields.Text(
        'Change'
    )
    description_event = fields.Text(
        'Reason'
    )
    description_effect = fields.Text(
        'Effect'
    )
    proximity_id = fields.Many2one(
        'change.management.proximity', 'Proximity',
        help='''
Proximity: This would typically state how close to the present time the change event is anticipated to happen
(e.g. for project changes Imminent, within stage, within project, beyond project). Proximity should be recorded
in accordance with the project's chosen scales or business continuity time scales.
        '''
    )
    change_response_ids = fields.One2many(
        'project.task', 'change_id', 'Response Ids'
    )
    change_response_count = fields.Integer(
        compute='_change_response_count', type='integer'
    )
    state = fields.Selection(
        _CHANGE_STATE, 'State', readonly=True
    )
    change_owner_id = fields.Many2one(
        'res.users', 'Change Manager',
        help='''
Change Manager: The person responsible for managing the change (there can be only one change owner per change),
change ownership is assigned to a managerial level, in case of business continuity to a C-level manager.
        '''
    )

    #
    # DEFINITIONS
    #

    _defaults = {
        'author_id': lambda s, cr, uid, c: uid,
        'date_registered': lambda *a: date.today().strftime('%Y-%m-%d'),
        'state': 'draft',
        'name': lambda s, cr, uid, c: s.pool.get('ir.sequence').get(cr, uid, 'change.management.change'),
        'color': '0'
    }

    def _subscribe_extra_followers(self, cr, uid, ids, vals, context=None):
        user_ids = [
            vals[x] for x in ['author_id', 'change_owner_id'] if x in vals and vals[x] != False
        ]
        if len(user_ids) > 0:
            self.message_subscribe_users(
                cr, uid, ids, user_ids=user_ids, context=context
            )

        changes = self.read(
            cr, uid, ids, ['message_follower_ids', 'change_response_ids']
        )
        for change in changes:
            if 'change_response_ids' in change and change['change_response_ids']:
                task_ob = self.pool.get('project.task')
                task_ob.message_subscribe(
                    cr, uid, change['change_response_ids'], change['message_follower_ids'], context=context
                )

    def write(self, cr, uid, ids, vals, context=None):
        ret = super(change_management_change, self).write(cr, uid, ids, vals, context)
        self._subscribe_extra_followers(cr, uid, ids, vals, context)
        return ret

    def create(self, cr, uid, vals, context=None):
        change_id = super(change_management_change, self).create(cr, uid, vals, context)
        self._subscribe_extra_followers(cr, uid, [change_id], vals, context)
        return change_id
