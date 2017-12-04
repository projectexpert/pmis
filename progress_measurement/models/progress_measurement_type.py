# -*- coding: utf-8 -*-
# © 2014-17 Eficent Business and IT Consulting Services S.L.
# © 2016 Matmoz d.o.o.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models
from odoo.exceptions import ValidationError


class ProgressMeasurementType(models.Model):

    _name = "progress.measurement.type"
    _description = 'Progress Measurement Type'

    @api.constrains('default_max_value')
    @api.multi
    def _check_default_max_value(self):
        for item in self:
            if item.default_max_value <= 0:
                return ValidationError(
                    'The maximum value must be greater than 0')

    @api.constrains('is_percent', 'default_max_value')
    @api.multi
    def _check_is_percent_default_max_value(self):
        for item in self:
            if item.is_percent is True and item.default_max_value > 100:
                return ValidationError(
                    'The maximum percentage must not exceed 100')

    @api.constrains('precision')
    @api.multi
    def _check_precision(self):
        for item in self:
            if item.precision <= 0:
                return ValidationError(
                    'The precision value must be greater than 0')

    @api.constrains('precision', 'default_max_value')
    @api.multi
    def _check_is_default_max_value_greater_than_precision(self):
        for item in self:
            if item.precision > item.default_max_value:
                return ValidationError(
                    'Default maximum value must be greater than precision '
                    'value')
        return True

    @api.model
    def _check_default(self, vals):
        if 'is_default' in vals:
            if vals['is_default'] is True:
                other_default = self.search([('is_default', '=', True)])
                if other_default:
                    raise ValidationError(
                        'Only one default measurement type '
                        'can exist.')

    name = fields.Char('Name', size=32, required=True, translate=True,
                       help="Name given to the progress measurement type")

    default_max_value = fields.Float('Default Maximum Value',
                                     help="Maximum value that is "
                                          "permitted for the object being "
                                          "measured as a total measure of "
                                          "progress.")
    precision = fields.Float('Precision',
                             help="Value of increments permitted"
                                  "for the given progress measurement type "
                                  "measured as a total measure of progress.")
    active = fields.Boolean('Active', default=True,
                            help="Indicates that this type of progress can "
                            "be used")

    is_percent = fields.Boolean('Percentage',
                                help="Indicates that progress measurements of "
                                     "this type are "
                                     "entered on a percent basis")
    is_default = fields.Boolean('Default measurement type',
                                help="Indicates that this progress "
                                     "measurements is to be used by default")

    _sql_constraints = [('progress_measurement_type_name_unique',
                         'unique(name)', 'Progress type name already exists')]

    @api.model
    def create(self, vals):
        self._check_default(vals)
        return super(ProgressMeasurementType, self).create(vals)

    @api.multi
    def write(self, vals):
        self._check_default(vals)
        return super(ProgressMeasurementType, self).write(vals)

    @api.onchange('is_percent')
    def on_change_is_percent(self):
        for rec in self:
            if self.is_percent is True:
                self.default_max_value = 100
