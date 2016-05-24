# -*- coding: utf-8 -*-
# © 2015 MATMOZ d.o.o.. <info@matmoz.si>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

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
