# -*- coding: utf-8 -*-
# Copyright 2017 Eficent Business and IT Consulting Services S.L.
# Copyright 2017 Luxim d.o.o.
# Copyright 2017 Matmoz d.o.o.
# Copyright 2017 Deneroteam.
# Copyright 2017 Serpent Consulting Services Pvt. Ltd.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo.addons.analytic_resource_plan.tests import \
    test_analytic_resource_plan


class TestAnalyticResourcePlanStock(
        test_analytic_resource_plan.TestAnalyticResourcePlan):

    def setUp(cls):
        super(TestAnalyticResourcePlanStock, cls).setUp()
        cls.location = cls.env['stock.location'].create({
            'name': 'ACC',
            'usage': 'internal',
            'analytic_account_id': cls.account_id.id})
        cls.account_id.location_id = cls.location
        cls.account_id.picking_type_id = cls.env.ref('stock.picking_type_in')

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
        # recomputing here as no relation to the pickings in this module
        # to put in the api depends
        cls.assertEqual(cls.resource_plan_line.incoming_qty, 5.0,
                        'Bad Incoming Qty')
        cls.assertEqual(cls.resource_plan_line.virtual_available, 5.0,
                        'Bad virtual Qty')
        picking_in.action_done()
        cls.assertEqual(cls.resource_plan_line.qty_available, 5.0,
                        'Bad QTY Available')
        cls.assertEqual(cls.resource_plan_line.incoming_done_qty, 5.0,
                        'Bad Incoming done Qty')
        picking_out = cls.env['stock.picking'].create({
            'picking_type_id': cls.env.ref('stock.picking_type_out').id,
            'location_id': cls.location.id,
            'location_dest_id': cls.account_id.location_id.id})
        cls.env['stock.move'].create({
            'name': '/',
            'product_id': cls.product.id,
            'product_uom_qty': 4.0,
            'analytic_account_id': cls.account_id.id,
            'picking_id': picking_out.id,
            'product_uom': cls.product.uom_id.id,
            'location_id': cls.location.id,
            'location_dest_id':
                cls.env.ref('stock.stock_location_customers').id,
        })
        picking_out.action_confirm()
        cls.assertEqual(cls.resource_plan_line.virtual_available, 1.0,
                        'Bad Qty available')
        cls.assertEqual(cls.resource_plan_line.outgoing_qty, 4.0,
                        'Bad Incoming done Qty')
        picking_out.action_done()
        cls.assertEqual(cls.resource_plan_line.outgoing_done_qty, 4.0,
                        'Bad outgoing done Qty')
