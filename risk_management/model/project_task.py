# -*- coding: utf-8 -*-
# Copyright (C) 2011-2015 ValueDecision Ltd <http://www.valuedecision.com>.
# Copyright (C) 2015 Neova Health <http://www.neovahealth.co.uk>.
# Copyright (C) 2015 Matmoz d.o.o. <http://www.matmoz.si>.
# Copyright (C) 2017 Luxim d.o.o. <http://www.luxim.si>.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openerp import api, models, fields


class ProjectTask (models.Model):
    _name = 'project.task'
    _inherit = 'project.task'

    risk_id = fields.Many2one(
        'risk.management.risk', 'Action on Risk', readonly=True,
        help="Task is an action on a risk identified by this label."
    )


class ProjectProject (models.Model):
    _name = 'project.project'
    _inherit = 'project.project'

    risk_ids = fields.One2many(
        'risk.management.risk',
        'project_id',
        'Project Risks'
    )

    risk_count = fields.Integer(
        compute='_risk_count', type='integer'
    )


    @api.depends('risk_ids')
    def _risk_count(self):
        for record in self:
            record.risk_count = len(record.risk_ids)
