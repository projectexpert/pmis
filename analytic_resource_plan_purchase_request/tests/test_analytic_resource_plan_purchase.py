# -*- coding: utf-8 -*-
# Copyright 2017 Eficent Business and IT Consulting Services S.L.
# Copyright 2017 Luxim d.o.o.
# Copyright 2017 Matmoz d.o.o.
# Copyright 2017 Deneroteam.
# Copyright 2017 Serpent Consulting Services Pvt. Ltd.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo.addons.analytic_resource_plan_stock.tests import \
    test_analytic_resource_plan_stock


class TestAnalyticResourcePlanPurchase(
        test_analytic_resource_plan_stock.TestAnalyticResourcePlanStock):

    def setUp(cls):
        super(TestAnalyticResourcePlanPurchase, cls).setUp()

    def test_res_purchase(cls):
        cls.assertEqual(cls.resource_plan_line.qty_available, 0.0,
                        'Showing qty where there is not')
        cls.assertEqual(cls.resource_plan_line.request_state,
                        'none', 'should no request')
        cls.resource_plan_line.action_button_confirm()
        cls.assertEqual(cls.resource_plan_line.request_state, 'draft',
                        'should draft request')
        purchase_request_line = \
            cls.resource_plan_line.purchase_request_lines[0]
        purchase_request = purchase_request_line.request_id
        purchase_request.button_to_approve()
        purchase_request.button_approved()
        cls.assertEqual(
            cls.resource_plan_line.request_state, 'approved',
            'should approved request')
        cls.assertEqual(
            cls.resource_plan_line.requested_qty, 1.0, 'requested wrong qty')
        cls.resource_plan_line.action_button_draft()
        cls.assertEqual(
            cls.resource_plan_line.request_state,
            'rejected', 'should rejected request')
