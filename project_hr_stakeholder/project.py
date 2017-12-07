# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2011 Eficent (<http://www.eficent.com/>)
#              <contact@eficent.com>
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

from openerp import tools
from openerp import fields, models, api
from openerp.tools.translate import _


class Project(models.Model):
    _name = "project.project"
    _inherit = "project.project"

    stakeholder_ids = fields.One2many(
        comodel_name='project.hr.stakeholder',
        inverse_name='project_id',
        string='Stakeholders'
    )

    stakeholders_count = fields.Integer(
        compute='_compute_stakehold_count', type='integer'
    )

    @api.depends('stakeholder_ids')
    def _compute_stakehold_count(self):
        for record in self:
            record.stakeholders_count = len(record.stakeholder_ids)
