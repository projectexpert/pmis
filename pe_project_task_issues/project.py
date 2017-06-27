# -*- encoding: utf-8 -*-

from openerp import models, fields, api


class Task(models.Model):
    _inherit = 'project.task'

    issue_ids = fields.One2many(
        'project.issue', 'task_id', string="Issues")

