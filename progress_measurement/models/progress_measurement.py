# -*- coding: utf-8 -*-
# © 2014-17 Eficent Business and IT Consulting Services S.L.
# © 2016 Matmoz d.o.o.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
import time
from odoo import api, fields, models
from odoo.exceptions import ValidationError


class ProgressMeasurement(models.Model):

    _name = "progress.measurement"
    _description = 'Progress Measurement'

    @api.multi
    @api.constrains('value', 'progress_type')
    def _check_is_value_less_than_max(self):
        for item in self:
            if item.progress_measurement_type:
                if item.value > item.progress_measurement_type.\
                        default_max_value:
                    raise ValidationError('Error! The value must be less than '
                                          'the maximum permitted defined in '
                                          'the progress measurement type')

    @api.multi
    @api.constrains('value', 'progress_type')
    def _check_is_valid_precision(self):
        for item in self:
            if item.progress_measurement_type:
                result = item.value % item.progress_measurement_type.precision
                if result != 0.0:
                    raise ValidationError('The value is entered in a higher '
                                          'precision to that defined in the'
                                          ' progress measurement type')
        return True

    name = fields.Char('Description', size=32, required=False,
                       help="Description given to the measure")
    communication_date = fields.Date('Communication date', required=True,
                                     help="Date when the measurement "
                                     "was communicated",
                                     default=time.strftime('%Y-%m-%d'))
    communication_date_print = fields.Char('Communication Date', size=32,
                                           required=True)
    value = fields.Float('Value', required=True, help="Value of the "
                                                      "measure")
    progress_measurement_type = fields.Many2one(
        'progress.measurement.type', 'Progress Measurement Type',
        required=True)
    user_id = fields.Many2one('res.users', 'Entered by', required=True,
                              default=lambda self: self.env.uid)

    @api.model
    def create(self, vals):
        vals['communication_date_print'] = vals['communication_date']
        return super(ProgressMeasurement, self).create(vals)

    @api.multi
    def write(self, vals):
        if 'communication_date' in vals:
            vals['communication_date_print'] = vals['communication_date']
        return super(ProgressMeasurement, self).write(vals)
