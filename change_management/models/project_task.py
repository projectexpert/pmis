# -*- coding: utf-8 -*-
# Copyright (C) 2017 Matmoz d.o.o. (<http://www.matmoz.si>).
# Copyright (C) 2018 Luxim d.o.o. (<https://www.luxim.si>).
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openerp import api, models, fields


class ProjectTask (models.Model):
    _name = 'project.task'
    _inherit = 'project.task'

    change_id = fields.Many2one(
        comodel_name='change.management.change',
        string='Request',
        readonly=False,
        help="Origined from this request.",
    )
    # topic = fields.Char(
    #     string='Topic/User Story',
    #     required=True,
    # )
    current_sit = fields.Char(
        string="Curent situation",
        required=False
    )
    desired_sit = fields.Char(
        string="Desired situation",
        required=False
    )

    # @api.onchange('topic')
    # def on_change_topic(self):
    #     if self.topic:
    #         self.name = self.topic
