# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Enterprise Management Solution
#    risk_management Module
#    Copyright (C) 2011-2015 ValueDecision Ltd <http://www.valuedecision.com>.
#    Copyright (C) 2015 Neova Health <http://www.neovahealth.co.uk>.
#    Copyright (C) 2015 Matmoz d.o.o. <http://www.matmoz.si>.
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

_RISK_STATE = [('draft', 'Draft'), ('active', 'Active'), ('closed', 'Closed')]


class RiskManagementRiskCategory (models.Model):
    _name = 'risk.management.category'
    _description = 'Risk log category table'

    name = fields.Char(string='Risk Category', size=64, required=True)


class RiskManagementRiskResponseCategory (models.Model):
    _name = 'risk.management.response.category'
    _description = 'Risk log response category table'

    type = fields.Selection(
        [('threat', 'Threat'), ('opportunity', 'Opportunity')], 'Type'
    )
    name = fields.Char(string='Response Category', size=64, required=True)


class RiskManagementProximity (models.Model):
    _name = 'risk.management.proximity'
    _description = 'Risk log proximity table'

    name = fields.Char(string='Proximity', size=64, required=True)


class RiskManagementRisk (models.Model):
    _name = 'risk.management.risk'
    _description = 'Risk'
    _inherit = ['mail.thread', 'ir.needaction_mixin']

    _track = {
        'state': {
            'risk.mt_risk_draft': (
                lambda self, cr, uid, obj, ctx=None: obj['state'] in ['draft']
            ),
            'risk.mt_risk_active': (
                lambda self, cr, uid, obj, ctx=None: obj['state'] in ['active']
            ),
            'risk.mt_risk_closed': (
                lambda self, cr, uid, obj, ctx=None: obj['state'] in ['closed']
            )
        }
    }

    @api.depends('risk_response_ids')
    def _risk_response_count(self):
            for record in self:
                record.risk_response_count = len(record.risk_response_ids)

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

    @api.one
    def set_state_draft(self):
        return self.write({'state': 'draft'})

    @api.one
    def set_state_active(self):
        return self.write({'state': 'active'})

    @api.one
    def set_state_closed(self):
        return self.write({'state': 'closed'})

    name = fields.Char(
        'Risk Id', size=64, required=True, readonly=True,
        states={'draft': [('readonly', False)]}, select=True,
        help='''
Risk label. Can be changed as long as risk is in state 'draft'.
'''
    )
    description = fields.Char(
        string='Risk Description', size=64, help='''
Short description of the Risk.

Project risks are characteristics, circumstances or
features of the project environment that may have an
adverse effect on the project or the quality of the
deliverables.

Project assumptions are knowledge about the project
that is taken as being true or correct for the purpose
of project planning. Assumptions are made to allow
planning to proceed with limited information about
certain elements that are vital to the management of
the project. Assumptions must be tested prior to
finalising the Project Plan.
'''
    )
    project_id = fields.Many2one(
        'project.project', 'Project', required=True
    )
    author_id = fields.Many2one(
        'res.users', 'Author', required=True
    )
    color = fields.Integer(
        'Color'
    )
    date_registered = fields.Date(
        'Date Registered', required=True,
        help="Date of the Risk registered. Auto populated."
    )
    date_modified = fields.Date(
        'Date Modified', help="Date of last update."
    )
    risk_category_id = fields.Many2one(
        'risk.management.category', 'Risk Category', required=True,
        help='''
Risk Category: The type of risk in terms of the project's or business' chosen
categories (e.g. Schedule, quality, legal etc.)
'''
    )
    description_cause = fields.Text(
        'Cause'
    )
    description_event = fields.Text(
        'Event'
    )
    description_effect = fields.Text(
        'Effect'
    )
    impact_inherent = fields.Integer(
        'Inherent Impact', required=True,
        help='''
Impact: The result of a particular threat or opportunity actually occurring,
or the anticipation of such a result. This is the pre-response value, common
used scales are 1 to 10 or 1 to 100.
'''
    )
    impact_residual = fields.Integer(
        'Residual Impact', required=True,
        help='''
Impact: The result of a particular threat or opportunity actually occurring,
or the anticipation of such a result. This is the post-response value, common
used scales are 1 to 10 or 1 to 100.
'''
    )
    probability_inherent = fields.Integer(
        'Inherent Probability', required=True,
        help='''
Probability: The evaluated likelihood of a particular threat or opportunity
actually happening, including a consideration of the frequency with which this
may arise. This is the pre-response value, common used scales are 1 to 10
or 1 to 100.
'''
    )
    probability_residual = fields.Integer(
        'Residual Probability', required=True,
        help='''
Probability: The evaluated likelihood of a particular threat or opportunity
actually happening, including a consideration of the frequency with which this
may arise. This is the post-response value, common used scales are 1 to 10
or 1 to 100.
'''
    )
    expected_value_inherent = fields.Float(
        compute='_calculate_expected_inherent_value', method=True,
        string='Expected Inherent Value', store=True,
        help='''
Expected Value. Cost of inherent impact * inherent probability. This is the
pre-response value.
'''
    )
    expected_value_residual = fields.Float(
        compute='_calculate_expected_residual_value', method=True,
        string='Expected Residual Value', store=True,
        help='''
Expected Value. Cost of residual impact * residual probability. This is the
post-response value.
'''
    )
    proximity_id = fields.Many2one(
        'risk.management.proximity', 'Proximity',
        help='''
Proximity: This would typically state how close to the present time the risk
event is anticipated to happen (e.g. for project risks Imminent, within stage,
within project, beyond project). Proximity should be recorded in accordance
with the project's chosen scales or business continuity time scales.
'''
    )
    risk_response_category_id = fields.Many2one(
        'risk.management.response.category', 'Response Category',
        help='''
Risk Response Categories: How the project will treat the risk in terms of
the project's (or business continuity planning) chosen categories.
'''
    )
    risk_response_ids = fields.One2many(
        'project.task', 'risk_id', 'Response Ids'
    )
    risk_response_count = fields.Integer(
        compute='_risk_response_count', type='integer'
    )
    state = fields.Selection(
        _RISK_STATE, 'State', readonly=True,
        help='''
A risk can have one of these three states: draft, active, closed.
'''
    )
    risk_owner_id = fields.Many2one(
        'res.users', 'Owner',
        help='''
Risk Owner: The person responsible for managing the risk (there can be only
one risk owner per risk), risk ownership is assigned to a managerial level,
in case of business continuity to a C-level manager.
'''
    )

    _defaults = {
        'author_id': lambda s, cr, uid, c: uid,
        'date_registered': lambda *a: date.today().strftime('%Y-%m-%d'),
        'state': 'draft',
        'impact_inherent': 0,
        'impact_residual': 0,
        'probability_inherent': 0,
        'probability_residual': 0,
        'name': lambda s, cr, uid, c: s.pool.get('ir.sequence').get(
            cr, uid, 'risk.management.risk'
        ),
        'color': '0'
    }

    def _subscribe_extra_followers(self, cr, uid, ids, vals, context=None):
        user_ids = [vals[x] for x in [
            'author_id', 'risk_owner_id'
        ] if x in vals and vals[x] != False
        ]
        if len(user_ids) > 0:
            self.message_subscribe_users(
                cr, uid, ids, user_ids=user_ids, context=context
            )

        risks = self.read(
            cr, uid, ids, ['message_follower_ids', 'risk_response_ids']
        )
        for risk in risks:
            if 'risk_response_ids' in risk and risk['risk_response_ids']:
                task_ob = self.pool.get('project.task')
                task_ob.message_subscribe(
                    cr, uid, risk['risk_response_ids'],
                    risk['message_follower_ids'], context=context
                )

    def write(self, cr, uid, ids, vals, context=None):
        ret = super(risk_management_risk, self).write(
            cr, uid, ids, vals, context
        )
        self._subscribe_extra_followers(cr, uid, ids, vals, context)
        return ret

    def create(self, cr, uid, vals, context=None):
        risk_id = super(risk_management_risk, self).create(
            cr, uid, vals, context
        )
        self._subscribe_extra_followers(cr, uid, [risk_id], vals, context)
        return risk_id
