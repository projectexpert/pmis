# -*- coding: utf-8 -*-
# © 2014-17 Eficent Business and IT Consulting Services S.L.
# © 2016 Matmoz d.o.o.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo.tests.common import TransactionCase
from odoo import fields
from odoo.exceptions import ValidationError


class TestProgressMeasurement(TransactionCase):

    def setUp(self):
        super(TestProgressMeasurement, self).setUp()
        self.measurement_type = self.env['progress.measurement.type']
        self.progress_measurement = self.env['progress.measurement']

        self.measurement_type_id = self.measurement_type.create({
            'name': 'Test Progress Measurement Type',
            'default_max_value': 100.0,
            'precision': 10.0,
            'active': True,
            'is_percent': True,
            'is_default': True
        })
        self.progress_measurement_id = self.progress_measurement.create({
            'name': 'Test Progress Measurement',
            'communication_date': fields.Date.today(),
            'communication_date_print': 'Communication Date',
            'value': 10.0,
            'progress_measurement_type': self.measurement_type_id.id,
            'user_id': self.env.user.id
        })

    def test_progress_measurement(self):
        with self.assertRaises(ValidationError):
            self.measurement_type.create({
                'name': 'Test Progress Measurement Type',
                'default_max_value': 100.0,
                'precision': 101.0,
                'active': True,
                'is_percent': True,
                'is_default': True
            })
        self.assertEquals(
            self.progress_measurement_id.communication_date_print,
            self.progress_measurement_id.communication_date
        )
