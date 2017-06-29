# -*- encoding: utf-8 -*-

from openerp import models, fields


class Project(models.Model):
    _inherit = 'project.project'

    page_ids = fields.Many2many(
        'document.page',
        'project_docu_rel',
        'project_id',
        'page_id',
        'Document pages'
    )


class Task(models.Model):
    _inherit = 'project.task'

    page_ids = fields.Many2many(
        'document.page',
        'task_page_rel',
        'task_id',
        'page_id',
        'Document pages'
    )
