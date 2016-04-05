# -*- encoding: utf-8 -*-
##############################################################################
#
# Copyright (c) 2013 Matmoz d.o.o. (info at matmoz.si)
#                          All Rights Reserved.
#
# WARNING: This program as such is intended to be used by professional
# programmers who take the whole responsability of assessing all potential
# consequences resulting from its eventual inadequacies and bugs
# End users who are looking for a ready-to-use solution with commercial
# garantees and support are strongly adviced to contract a Free Software
# Service Company
#
# This program is Free Software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#
##############################################################################

from openerp import api, models, fields


class LeadProject(models.Model):
    _inherit = 'crm.lead'

    project_id = fields.Many2one('project.project', 'Project')


class ProjectLead(models.Model):
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
