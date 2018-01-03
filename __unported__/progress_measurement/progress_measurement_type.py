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


class progress_measurement_type(osv.osv):

    _name = "progress.measurement.type"
    _description = 'Progress Measurement Type'

    def _check_default_max_value(self, cr, uid, ids):
        for item in self.browse(cr, uid, ids):
            if item.default_max_value <= 0:
                    return False
        return True

    def _check_is_percent_default_max_value(self, cr, uid, ids):
        for item in self.browse(cr, uid, ids):
            if item.is_percent is True and item.default_max_value > 100:
                    return False
        return True

    def _check_precision(self, cr, uid, ids):
        for item in self.browse(cr, uid, ids):
            if item.precision <= 0:
                    return False
        return True

    def _check_is_default_max_value_greater_than_precision(self, cr, uid, ids):
        for item in self.browse(cr, uid, ids):
            if item.precision > item.default_max_value:
                    return False
        return True

    def _check_default(self, cr, uid, vals, context=None):

        if 'is_default' in vals:
            if vals['is_default'] is True:
                other_default = self.search(
                    cr, uid, [('is_default', '=', True)], context=context)
                if other_default:
                    raise osv.except_osv(
                        _('Error!'),
                        _('Only one default measurement type can exist.')
                    )

    _columns = {
        'name': fields.char(
            'Name', size=32, required=True, translate=True,
            help="Name given to the progress measurement type"
        ),

        'default_max_value': fields.float(
            'Default Maximum Value',
            help="Maximum value that is permitted for the object being "
            "measured as a total measure of progress."
        ),
        'precision': fields.float(
            'Precision',
            help="Value of increments permitted for the given progress"
                 "measurement type measured as a total measure of progress."
        ),
        'active': fields.boolean(
            'Active',
            help="Indicates that this type of progress can be used"
        ),

        'is_percent': fields.boolean(
            'Percentage',
            help="Indicates that progress measurements of this type are "
            "entered on a percent basis"
        ),
        'is_default': fields.boolean(
            'Default measurement type',
            help="""
            Indicates that this progress measurements is to be used by default
            """
        ),
    }

    _sql_constraints = [(
        'progress_measurement_type_name_unique',
        'unique(name)',
        'Progress type name already exists'
    )]

    _constraints = [
        (
            _check_default_max_value,
            'Error! The maximum value must be greater than 0',
            ['default_max_value']
        ),
        (
            _check_is_percent_default_max_value,
            'Error! The maximum percentage must not exceed 100',
            ['is_percent', 'default_max_value']
        ),
        (
            _check_precision,
            'Error! The precision value must be greater than 0',
            ['precision']
        ),
        (
            _check_is_default_max_value_greater_than_precision,
            'Error! Default maximum value must be higher than precision value',
            ['precision', 'default_max_value']
        ),

    ]

    _defaults = {
        'active': True,
    }

    def create(self, cr, uid, vals, *args, **kwargs):

        context = kwargs.get('context', {})
        self._check_default(cr, uid, vals, context)
        return super(progress_measurement_type, self).create(
            cr, uid, vals, *args, **kwargs)

    def write(self, cr, uid, ids, vals, context=None):
        if context is None:
            context = {}

        self._check_default(cr, uid, vals, context)
        return super(progress_measurement_type, self).write(
            cr, uid, ids, vals, context=context)

    def on_change_is_percent(self, cr, uid, id, is_percent, context=None):
        res = {}
        if is_percent is True:
            res['value'] = {'default_max_value': 100}
        return res

progress_measurement_type()
