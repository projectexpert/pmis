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
import time
from openerp.osv import fields, osv


class progress_measurement(osv.osv):

    _name = "progress.measurement"
    _description = 'Progress Measurement'

    def _check_is_value_less_than_max(self, cr, uid, ids):
        for item in self.browse(cr, uid, ids):
            if item.progress_measurement_type:
                if (
                    item.value >
                    item.progress_measurement_type.default_max_value
                ):
                    return False
        return True

    def _check_is_valid_precision(self, cr, uid, ids):
        for item in self.browse(cr, uid, ids):
            if item.progress_measurement_type:
                result = item.value % item.progress_measurement_type.precision
                if result != 0.0:
                    return False
        return True

    _columns = {
        'name': fields.char('Description', size=32, required=False,
                            help="Description given to the measure"),
        'communication_date': fields.date(
            'Communication date', required=True,
            help="Date when the measurement was communicated"),
        'communication_date_print': fields.char(
            'Communication Date', size=32, required=True),

        'value': fields.float(
            'Value', required=True, help="Value of the measure"),
        'progress_measurement_type': fields.many2one(
            'progress.measurement.type', 'Progress Measurement Type',
            required=True
        ),
        'user_id': fields.many2one('res.users', 'Entered by', required=True),
    }

    _order = 'communication_date'

    _constraints = [
        (
            _check_is_value_less_than_max,
            'Error! The value must be less than the maximum permitted '
            'defined in the progress measurement type',
            ['value', 'progress_type']
        ),
        (
            _check_is_valid_precision,
            'Error! The value is entered in a higher precision to that'
            'defined in the progress measurement type',
            ['value', 'progress_type']
        ),

    ]

    _defaults = {
        'communication_date': time.strftime('%Y-%m-%d'),
        'user_id': lambda self, cr, uid, context: uid,
    }

    def create(self, cr, uid, vals, *args, **kwargs):

        vals['communication_date_print'] = vals['communication_date']

        return super(progress_measurement, self).create(
            cr, uid, vals, *args, **kwargs)

    def write(self, cr, uid, ids, vals, context=None):

        if context is None:
            context = {}
        if 'communication_date' in vals:
            vals['communication_date_print'] = vals['communication_date']

        return super(progress_measurement, self).write(
            cr, uid, ids, vals, context=context)


progress_measurement()
