# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2014 Eficent (<http://www.eficent.com/>)
#              <contact@eficent.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
from openerp import fields, models, api, _

class earned_value_task_graphs(models.TransientModel):
    _name = "earned.value.task.graphs"
    _description = "Earned Value Graphs"

    project_id = fields.Many2one('project.project',
                                 'Project', required=True)

    @api.multi
    def earned_value_graphs_open_window(self):
        """
        Opens Earned Value report
        """
        self.ensure_one()
        # Update the project EVM
        records = self.project_id.update_project_evm()

        return {
            'domain': "[('id','in', ["+','.join(map(str, records))+"])]",
            'name': _('Earned Value Records'),
            'view_type': 'form',
            'view_mode': 'graph,tree,form',
            'res_model': 'project.evm.task',
            'view_id': False,
            'context': False,
            'type': 'ir.actions.act_window'
        }

