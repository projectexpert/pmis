# -*- coding: utf-8 -*-
# Copyright 2017 Eficent Business and IT Consulting Services S.L.
#  - Jordi Ballester Alomar
# Copyright 2017 MATMOZ d.o.o.
#  - Matjaž Mozetič
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo.tests import common
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from datetime import datetime


class TestPurchaseStockAnalytic(common.TransactionCase):

    def setUp(self):
        super(TestPurchaseStockAnalytic, self).setUp()
        self.PurchaseOrder = self.env['purchase.order']
        self.AnalyticAccount = self.env['account.analytic.account']
        self.product_id_1 = self.env.ref('product.product_product_8')
        self.partner_id_2 = self.env.ref('base.res_partner_2')
        self.partner_id = self.env.ref('base.res_partner_1')
        self.analytic_account = self.AnalyticAccount.create({
            'name': 'Test Analytic Account',
        })
        self.po_vals = {
            'partner_id': self.partner_id.id,
            'order_line': [
                (0, 0, {
                    'name': self.product_id_1.name,
                    'product_id': self.product_id_1.id,
                    'product_qty': 5.0,
                    'product_uom': self.product_id_1.uom_po_id.id,
                    'price_unit': 500.0,
                    'account_analytic_id': self.analytic_account.id,
                    'date_planned': datetime.today().
                    strftime(DEFAULT_SERVER_DATETIME_FORMAT),
                })],
        }

    def test_purchase_stock_analytic(self):
        self.po = self.PurchaseOrder.create(self.po_vals)
        self.po.button_confirm()
        self.picking = self.po.picking_ids
        self.picking.force_assign()
        self.picking.do_new_transfer()
        self.picking.move_lines.analytic_account_id = self.analytic_account.id
        self.assertEqual(self.po.order_line.account_analytic_id.id,
                         self.picking.move_lines.analytic_account_id.id)
