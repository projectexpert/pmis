# -*- encoding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2013 Matmoz d.o.o. (<http://www.matmoz.si>)
#
#
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp import api, models, fields


class lead_project(models.Model):
    _inherit = 'crm.lead'

    project_id = fields.Many2one('project.project', 'Project')


class project_lead(models.Model):
    _inherit = 'project.project'

    @api.one
    def _project_lead_count(self):
        self.project_lead_count = self.env['crm.lead'].search_count(
            [('project_id', 'in', self.ids)]
        )

    lead_ids = fields.One2many(
        'crm.lead', 'project_id', 'Lead / Opportunity'
    )
    project_lead_count = fields.Integer(
        compute="_project_lead_count", string="Leads"
    )
