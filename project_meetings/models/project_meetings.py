# -*- coding: utf-8 -*-

from openerp import api, fields, models


class Meeting(models.Model):

    _inherit = 'calendar.event'

    project_id = fields.Many2one('project.project', 'Project')


class Project(models.Model):

    _inherit = "project.project"

    @api.one
    def _project_meeting_count(self):
        self.project_meeting_count = self.env['calendar.event'].search_count(
            [('project_id', 'in', self.ids)]
        )

    calendar_events = fields.One2many(
        'calendar.event', 'project_id', string='Meetings'
    )
    project_meeting_count = fields.Integer(
        compute="_project_meeting_count", string="Meetings"
    )
