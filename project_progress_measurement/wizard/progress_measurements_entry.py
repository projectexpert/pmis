# -*- coding: utf-8 -*-
# Copyright 2014-17 Eficent Business and IT Consulting Services S.L.
#        <contact@eficent.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models, _


class ProgressMeasurementsEntry(models.TransientModel):
    """
    For Bulk entry of progress measurements
    """
    _name = "progress.measurements.entry"
    _description = "Progress measurements entry"

    communication_date = fields.Date(
        'Communication date',
        required=True,
        default=fields.Date.context_today
    )
    progress_measurement_type_id = fields.Many2one(
        'progress.measurement.type',
        'Progress Measurement Type',
        required=True
    )

    @api.multi
    def progress_measurements_open_window(self):

        res = []
        project_obj = self.env['project.project']
        meas_obj = self.env['project.progress.measurement']
        record_ids = self._context and self._context.get('active_ids', False)
        project_id = project_obj.browse(record_ids)
        project_ids = project_id._get_project_wbs()
        data = self.read()[0]
        communication_date = data.get('communication_date', False)
        progress_measurement_type_id = (
            data.get('progress_measurement_type_id', False) and
            data['progress_measurement_type_id'][0] or
            False
        )
        self._cr.execute('SELECT DISTINCT ON (a.project_id) project_id, id,'
                         'communication_date, value'
                         'FROM project_progress_measurement AS a'
                         'WHERE a.project_id IN %s'
                         'AND a.progress_measurement_type = %s'
                         'ORDER BY a.project_id, a.communication_date DESC',
                         (tuple(project_ids), progress_measurement_type_id))
        results = self._cr.fetchall()

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
                if measurements[project_id]['communication_date'
                                            ] == communication_date:
                    res.append(measurements[project_id]['id'])
                else:
                    vals['value'] = measurements[project_id]['value']
                    res.append(meas_obj.create(vals))
            else:
                vals['value'] = 0
                res.append(meas_obj.create(vals))
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
