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

from openerp.osv import orm, fields, osv
from openerp.tools.translate import _


class resource_plan_line_change_state(osv.osv_memory):

    _name = "resource.plan.line.change.state"
    _description = "Change state of resource plan line"

    _columns = {
        'state': fields.selection(
            [('draft', 'Draft'),
             ('confirm', 'Confirmed')], 'Status',
            select=True, required=True,
            help=' * The \'Draft\' status is used when a user is encoding '
                 'a new and unconfirmed resource plan line. '
                 '\n* The \'Confirmed\' status is used for to confirm the '
                 'resource plan line by the user.'),
    }

    def change_state_confirm(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        data = self.read(cr, uid, ids, [], context=context)[0]
        record_ids = context and context.get('active_ids', False)
        line_plan_obj = self.pool.get('analytic.resource.plan.line')
        new_state = data.get('state', False)
        if new_state == 'draft':
            line_plan_obj.action_button_draft(cr, uid, record_ids,
                                              context=context)
        elif new_state == 'confirm':
            line_plan_obj.action_button_confirm(cr, uid, record_ids,
                                                context=context)
        return {
            'domain': "[('id','in', ["+','.join(map(str, record_ids))+"])]",
            'name': _('Resource Planning Lines'),
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'analytic.resource.plan.line',
            'view_id': False,
            'context': False,
            'type': 'ir.actions.act_window'
        }
