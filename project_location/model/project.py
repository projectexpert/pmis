# -*- coding: utf-8 -*-
# © 2017 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models


class ProjectProject(models.Model):
    _inherit = 'project.project'

    @api.model
    def get_parent_stock_data(self):
        context = self.env.context
        res = {}
        if 'default_parent_id' in context and context['default_parent_id']:
            for project in self.search(
                    [
                        (
                                'analytic_account_id',
                                '=',
                                context['default_parent_id']
                        )
                    ]
            ):
                res['location_id'] = project.location_id
                res['dest_address_id'] = project.dest_address_id
        return res

    @api.model
    def _default_dest_address(self):
        res = self.get_parent_stock_data()
        if 'dest_address_id' in res:
            return res['dest_address_id']
        else:
            return super(ProjectProject, self)._default_dest_address()

    location_id = fields.Many2one(related='analytic_account_id.location_id')
    dest_address_id = fields.Many2one(
        related='analytic_account_id.dest_address_id')
