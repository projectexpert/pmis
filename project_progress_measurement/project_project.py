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

from osv import fields, osv


class project(osv.osv):

    _inherit = "project.project"

    def _agg_progress_measurement_rate(self, cr, uid, ids, names, arg, context=None):

        res = dict([(id, 0.0) for id in ids])
        measurement_type_obj = self.pool.get('progress.measurement.type')
        def_meas_type = measurement_type_obj.search(cr, uid, [('is_default', '=', True)], context=context)
        if def_meas_type:
            cr.execute("""
            SELECT DISTINCT ON (PPM.project_id) PPM.project_id, PPM.value, PMT.default_max_value
            FROM project_progress_measurement as PPM
            INNER JOIN progress_measurement_type as PMT
            ON (PPM.progress_measurement_type = PMT.id)
            WHERE PMT.is_default = True
            AND project_id in %s
            ORDER BY PPM.project_id, PPM.communication_date DESC
            """, (tuple(ids),))
            for project_id, value, default_max_value in cr.fetchall():
                if default_max_value > 0.0:
                    res[project_id] = round(100 * (value / default_max_value), 2)
                else:
                    res[project_id] = 0.0
        return res

    _columns = {
        'progress_measurement_rate': fields.function(_agg_progress_measurement_rate,
                                                     string='Progress', type='float',
                                                     help="Percent of completion"),
        'progress_measurements': fields.one2many('project.progress.measurement',
                                                 'project_id',
                                                 'Measurements'),
    }

    def copy(self, cr, uid, id, default=None, context=None):

        if context is None:
            context = {}
        if default is None:
            default = {}

        default['progress_measurements'] = []

        return super(project, self).copy(cr, uid, id, default=default, context=context)

project()