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

from openerp.osv import fields, osv
from openerp.tools.translate import _

class earned_value_graphs(osv.osv_memory):
    """
    For Earned Value Management
    """
    _name = "earned.value.graphs"
    _description = "Earned Value Graphs"
    _columns = {
        'project_id': fields.many2one('project.project',
                                      'Project', required=True),
        'progress_measurement_type': fields.many2one('progress.measurement.type',
                                                     'Progress Measurement Type',
                                                     required=True),
    }

    def earned_value_graphs_open_window(self, cr, uid, ids, context=None):
        """
        Opens Earned Value report
        @param cr: the current row, from the database cursor,
        @param uid: the current user’s ID for security checks,
        @param ids: List of account chart’s IDs
        @return: dictionary of Earned Value window on given project
        """
        project_obj = self.pool.get('project.project')
        if context is None:
            context = {}
        data = self.read(cr, uid, ids, [], context=context)[0]
        project_id = data.get('project_id', False) and data['project_id'][0] or False
        progress_measurement_type = data.get('progress_measurement_type', False) and data['progress_measurement_type'][0] or False

        #Update the project EVM
        records = project_obj.update_project_evm(cr, uid, [project_id], progress_measurement_type, context)
        
        return {
            'domain': "[('id','in', ["+','.join(map(str, records))+"])]",
            'name': _('Earned Value Records'),
            'view_type': 'form',
            'view_mode': 'graph,tree,form',
            'res_model': 'project.evm',
            'view_id': False,
            'context': False,
            'type': 'ir.actions.act_window'
        }



earned_value_graphs()
