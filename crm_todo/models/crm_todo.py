# -*- coding: utf-8 -*-
# © 2015 MATMOZ d.o.o.. <info@matmoz.si>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openerp import models, fields


class project_task(models.Model):
    _inherit = 'project.task'

    lead_id = fields.Many2one('crm.lead', 'Lead / Opportunity')


class crm_todo(models.Model):
    _inherit = 'crm.lead'

    task_ids = fields.One2many('project.task', 'lead_id', 'Tasks')
