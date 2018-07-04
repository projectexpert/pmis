# -*- coding: utf-8 -*-
# Copyright 2017 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo.addons.analytic_resource_plan_stock_picking.tests import \
    test_analytic_resource_plan_stock_picking


class TestAnalyticResourcePlanStockPickingPurchaseRequest(
        test_analytic_resource_plan_stock_picking.
        TestAnalyticResourcePlanStockPicking):

    def setUp(cls):
        super(TestAnalyticResourcePlanStockPickingPurchaseRequest, cls).setUp()

    def test_analytic_resource_plan_stock_picking(cls):
        cls.resource_plan_line.unit_amount = 2.0
        upd_qty = cls.env['stock.change.product.qty'].create({
            'product_id': cls.resource_plan_line.product_id.id,
            'product_tmpl_id':
            cls.resource_plan_line.product_id.product_tmpl_id.id,
            'new_quantity': 1.0,
            'location_id': cls.env.ref('stock.stock_location_stock').id
        })
        upd_qty.change_product_qty()
        cls.resource_plan_line.action_button_confirm()
        purchase_request_line = \
            cls.resource_plan_line.purchase_request_lines[0]
        purchase_request = purchase_request_line.request_id
        purchase_request.button_to_approve()
        purchase_request.button_approved()
        cls.assertEqual(
            cls.resource_plan_line.request_state, 'approved',
            'should approved request')
        cls.assertEqual(
            cls.resource_plan_line.requested_qty, 1.0, 'bad qty requested')
