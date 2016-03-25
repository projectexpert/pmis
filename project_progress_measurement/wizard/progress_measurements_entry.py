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
import time


class progress_measurements_entry(osv.osv_memory):
    """
    For Bulk entry of progress measurements
    """
    _name = "progress.measurements.entry"
    _description = "Progress measurements entry"

    _columns = {
        'communication_date': fields.date('Communication date', required=True),
        'progress_measurement_type_id': fields.many2one('progress.measurement.type',
                                                        'Progress Measurement Type', required=True),
    }

    _defaults = {
        'communication_date': time.strftime('%Y-%m-%d'),
    }

    def progress_measurements_open_window(self, cr, uid, ids, context=None):

        if context is None:
            context = {}
        res = []

        project_obj = self.pool.get('project.project')
        meas_obj = self.pool.get('project.progress.measurement')

        record_ids = context and context.get('active_ids', False)
        project_ids = project_obj._get_project_wbs(cr, uid, record_ids, context=context)
        data = self.read(cr, uid, ids, [], context=context)[0]
        communication_date = data.get('communication_date', False)
        progress_measurement_type_id = (
            data.get('progress_measurement_type_id', False) and
            data['progress_measurement_type_id'][0] or
            False
        )

        cr.execute('SELECT DISTINCT ON (a.project_id) project_id, id, communication_date, value '
                   'FROM project_progress_measurement AS a '
                   'WHERE a.project_id IN %s '
                   'AND a.progress_measurement_type = %s '
                   'ORDER BY a.project_id, a.communication_date DESC',
                   (tuple(project_ids), progress_measurement_type_id))
        results = cr.fetchall()

        measurements = {}
        for result in results:
            measurements[result[0]] = {
                'id': result[1],
                'communication_date': result[2],
                'value': result[3],
            }

        for project_id in project_ids:
            vals = {
                'project_id': project_id,
                'communication_date': communication_date,
                'progress_measurement_type': progress_measurement_type_id,
            }
            if project_id in measurements.keys():
                if measurements[project_id]['communication_date'] == communication_date:
                    res.append(measurements[project_id]['id'])
                else:
                    vals['value'] = measurements[project_id]['value']
                    res.append(meas_obj.create(cr, uid, vals, context=context))
            else:
                vals['value'] = 0
                res.append(meas_obj.create(cr, uid, vals, context=context))

        return {
            'domain': "[('id','in', [" + ','.join(map(str, res)) + "])]",
            'name': _('Non-aggregated progress measurements'),
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'project.progress.measurement',
            'view_id': False,
            'context': False,
            'type': 'ir.actions.act_window'
        }


progress_measurements_entry()
