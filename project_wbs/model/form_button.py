# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2015 Matmoz (<http://www.matmoz.si/>)
#               <info@matmoz.si>
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
from openerp import models, api, _


class formView(models.Model):
    _inherit = 'project.project'

    @api.multi
    def button_save_data(self):
        return True

    @api.multi
    def action_open_view_project_form(self):
        context = self.env.context.copy()
        context['view_buttons'] = True
        view = {
            'name': _('Details'),
            'view_type': 'form',
            'view_mode': 'form,tree,kanban,gantt',
            'res_model': 'project.project',
            'view_id': False,
            'type': 'ir.actions.act_window',
            'target': 'current',
            'res_id': self.id,
            'context': context
        }
        return view
