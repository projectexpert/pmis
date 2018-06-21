# -*- coding: utf-8 -*-
# Copyright 2017 Eficent Business and IT Consulting Services S.L.
# Copyright 2017 Luxim d.o.o.
# Copyright 2017 Matmoz d.o.o.
# Copyright 2017 Deneroteam.
# Copyright 2017 Serpent Consulting Services Pvt. Ltd.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo.addons.analytic_resource_plan.tests import test_analytic_resource_plan


class TestAnalyticResourcePlanStock(
    test_analytic_resource_plan.TestAnalyticResourcePlan):

    def setUp(cls):
        super(TestAnalyticResourcePlanStock, cls).setUp()
        cls.location = cls.env['stock.location'].create({
                    'location_id': cls.env.ref('stock.stock_location_stock').id,
                    'name': 'ACC',
                    'usage': 'internal'
                })
        cls.account_id.location_id = cls.location.id

    def test_res_stock(cls):
        cls.assertEqual(cls.resource_plan_line.qty_available, 0.0,
                        'Showing qty where there is not')
        cls.resource_plan_line.action_button_confirm()

        picking_in = cls.env['stock.picking'].create({
            'picking_type_id': cls.env.ref('stock.picking_type_in').id,
            'location_id': cls.env.ref('stock.stock_location_suppliers').id,
            'location_dest_id': cls.account_id.location_id.id})
        cls.env['stock.move'].create({
            'name': '/',
            'product_id': cls.product.id,
            'product_uom_qty': 5.0,
            'analytic_account_id': cls.account_id.id,
            'picking_id': picking_in.id,
            'product_uom':  cls.product.uom_id.id,
            'location_id': cls.env.ref('stock.stock_location_suppliers').id,
            'location_dest_id': cls.account_id.location_id.id,
        })
        picking_in.action_confirm()
        cls.assertEqual(cls.resource_plan_line.incoming_qty, 5.0,
                        'Bad Incoming Qty')
        cls.assertEqual(cls.resource_plan_line.virtual_available, 5.0,
                        'Bad virtual Qty')

        upd_qty = cls.env['stock.change.product.qty'].create({
            'product_id': cls.product.id,
            'product_tmpl_id': cls.product.product_tmpl_id.id,
            'new_quantity': 10.0,
            'location_id': cls.account_id.location_id.id,
        })
        upd_qty.change_product_qty()
        cls.assertEqual(cls.resource_plan_line.incoming_done_qty, 10.0,
                        'WRONG incoming qty')
        cls.assertEqual(cls.resource_plan_line.virtual_available, 15.0,
                        'Wrong virtual qty')
