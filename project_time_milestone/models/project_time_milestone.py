# -*- coding: utf-8 -*-
#    Copyright (C) 2015 Eficent (Jordi Ballester Alomar)
#    Copyright (C) 2017 Matmoz d.o.o. (Matjaž Mozetič)
#    Copyright (C) 2017 Luxim d.o.o. (Matjaž Mozetič)
#    License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openerp import fields, models, api


class Task(models.Model):
    _inherit = 'project.task'

    milestone = fields.Boolean(
        string='Milestone',
        help="If the active field is set, the task is considered to be "
             "a milestone"
    )
    public_milestone = fields.Boolean(
        string='Public Milestone',
        help="If the active field is set, the task is considered to be a "
             "client-relevant milestone"
    )
    project_poc = fields.Float(
        string='Project percentage of completion',
        help="Percentage of completion for the linked project"
    )
    invoice_percentage = fields.Float(
        string='Invoice percentage',
        help="Percentage to invoice"
    )


class Project(models.Model):

    _inherit = "project.project"

    milestones = fields.One2many(
        comodel_name='project.task',
        inverse_name="project_id",
        string='Milestones',
        domain=[('milestone', '=', 'True')]
    )
